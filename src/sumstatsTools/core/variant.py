# File Name: variant.py
# Created By: ZW
# Created On: 2023-09-11
# Purpose: defines a data structure for a variant 
#   and its associated summary stats to be used in other tools. 


# library imports 
# -----------------------------------------------------------------------------

from math import erf, sqrt, log10, copysign
from typing import Tuple, List, Dict, Union, Literal


# object defintitions
# -----------------------------------------------------------------------------

# define the variant data type which is the base object in sumstats tools
class Variant:
    def __init__(self, chrom: str, pos: str, id: str, eff_allele: str,
                 other_allele: str, beta: str, beta_se: str,
                 zscore: str, pval: str, logp: str) -> None:
        self.chrom = chrom
        self.pos = pos
        self.id = id
        self.eff_allele = eff_allele
        self.other_allele = other_allele
        self.beta = beta
        self.beta_se = beta_se
        self.zscore = zscore
        self.pval = pval
        self.logp = logp

    # define custom string representation for object
    def __repr__(self) -> str:
        return (f"Variant(chrom={self.chrom} pos={self.pos} id={self.id} "
                f"eff_allele={self.eff_allele} other_allele={self.other_allele} "
                f"beta={self.beta} beta_se={self.beta_se} zscore={self.zscore} "
                f"pval={self.pval} logp={self.logp})"
                )



# primitive function definitions
# -----------------------------------------------------------------------------

# define a function to convert simple chromosome IDs (i.e. 1, 2, 3, X, ...)
# to ones that match UCSC (chr1, chr2, chr3, chrX, ...)
def make_ucsc_chrom(variant: Variant) -> None:
    if not variant.chrom.startswith('chr'):
        variant.chrom = "chr" + str(variant.chrom)

# define a function to convert UCSC pattern chromosome IDs (i.e. chr1, chr2, chr3, chrX, ...)
# to the simple ones often found in Broad Institute Genome Assemblies (1, 2, 3, X, ...)
def make_simple_chrom(variant: Variant) -> None:
    if variant.chrom.startswith('chr'):
        variant.chrom = variant.chrom[3:]


# define a function to calculate z-score (if possible) from beta and se values
# in a variant object. if either beta or se is empty, or a zscore already 
# exists, the function will not generate a value.
def compute_zscore(variant: Variant) -> None:
    if (variant.beta != '.' and variant.beta_se != '.' and variant.zscore == '.'):
        try:
            variant.zscore = str(float(variant.beta) / float(variant.beta_se))
        except ZeroDivisionError:
            variant.zscore = str(copysign(float('inf'), float(variant.beta)))


# define a function to calculate pvalues based on z-score in a variant object.
# the pvalues represented herein are two-tailed. logpvalues are computed as -1*log10(P)
def compute_pval_logpval(variant: Variant) -> None:
    # calculate pvalue from z-score using normal cdf
    if (variant.zscore != '.' and variant.pval == '.'):
        p: float = 2.0* (1.0 - 0.5 * (1.0 + erf(abs(float(variant.zscore)) / sqrt(2.0))))
        variant.pval = str(p)

    # calculate logp from pvalue where pvalue is not zero
    if (variant.pval != '.' and float(variant.pval) != 0):
        variant.logp = str(-1.0*log10(float(variant.pval)))
    
    # calculate logp from pvalue where pvalue is zero
    if (variant.pval != '.' and float(variant.pval) == 0):
        variant.logp = str(float('-inf'))



# high-level function definitions
# -----------------------------------------------------------------------------

# define function that generates a key, or a list of indices that correspond to the
# fields of a Variant object in a tuple of tokens representing the parsed file.
# this key can be passed to other functions to then generate Variant objects 
# efficiently through index lookups.
def generate_variant_key(name_map: Dict[str,Union[str,None]],
                         names: Tuple[str,...]) -> List[Union[int,Literal['.']]]:

    indices: List[Union[int, Literal['.']]] = []
    for key in name_map.keys():
        try:
            ind = names.index(name_map[key])
        except ValueError:
            ind = '.'
        
        indices.append(ind)
    return indices
    

# define a function that creates a Variant object from a tuple of tokens and a variant key dictionary
# which provides accessor functions based on the positions of columns passed in the original sumstats file
# the function also attempts to compute a zscore and pvalue for the variant if its missing but the necessary
# information is provided : (beta and se)
def variant_from_tokens(tokens: Tuple[str,...],
                        var_key: List[Union[int,Literal['.']]],
                        chrom_convert: Union[str,None]) -> Variant:
    
    # generate the variant object. run computations on zscore and pvalue
    args: List[str] = []
    for ind in var_key:
        if ind != '.':
            args.append(tokens[ind])
        else:
            args.append('.')

    var : Variant = Variant(*args)
    
    compute_zscore(var)
    compute_pval_logpval(var)

    # convert chroms if indicated
    if ((chrom_convert == None) or (chrom_convert == 'none')): pass
    elif chrom_convert == 'ucsc': make_ucsc_chrom(var)
    elif chrom_convert == 'simple': make_simple_chrom(var)
    else:
        raise ValueError("Chrom convert must be one of: None,'none','ucsc','simple'")

    # return the variant object
    return var

