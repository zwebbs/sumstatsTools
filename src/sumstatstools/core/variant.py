# File Name: variant.py
# Created By: ZW
# Created On: 2023-09-19
# Purpose: defines the variant object which has a contig, a position, a reference,
#  a name, allele, alternate allele, filter annotation, quality annotation, 
#  and info dictionary.

# library imports
# -----------------------------------------------------------------------------

from .stats import Beta, StdErr, Effect, ZScore, PValue, LogPValue
from .stats import compute_zscore, compute_pvalue, compute_logpvalue
from typing import Dict, Tuple, List, Literal, Union, Any
from .contig import Contig


# type aliases
# -----------------------------------------------------------------------------

Tokens = Tuple[str,...]
InfoT = Dict[str,Tuple[Any,...]]
Indices = List[Union[int,Literal['.']]]
ConvertChoices = Union[Literal['simple'],Literal['ucsc'],Literal['none']]


# object definitions
# -----------------------------------------------------------------------------

class Variant:
    # define initial configuration requiring 7 core attributes to be passed
    def __init__(self, contig: Contig, pos: int, ref: str, name: str,
                  alt: str, filt: str, qual: str, info: InfoT) -> None:
        self._contig = contig
        self._pos = pos
        self._name = name
        self._ref = ref
        self._alt = alt
        self._filt = filt
        self._qual = qual
        self._info = info

    # define getters and setters
    def get_contig(self) -> Contig:
        return self._contig

    def set_contig(self, new_contig: Contig) -> None:
        self._contig = new_contig

    def get_pos(self) -> int:
        return self._pos

    def set_pos(self, new_pos: int) -> None:
        self._pos = new_pos

    def get_name(self) -> str:
        return self._name
    
    def set_name(self, new_name: str) -> None:
        self._name = new_name

    def get_ref(self) -> str:
        return self._ref

    def set_ref(self, new_ref: str) -> None:
        self._ref = new_ref

    def get_alt(self) -> str:
        return self._alt

    def set_alt(self, new_alt: str) -> None:
        self._ref = new_alt

    def get_filt(self) -> str:
        return self._filt
    
    def set_filt(self, new_filt: str) -> None:
        self._filt = new_filt

    def get_qual(self) -> str:
        return self._qual

    def set_qual(self, new_qual: str) -> None:
        self._qual = new_qual

    def get_info(self) -> InfoT:
        return self._info
    
    def set_info(self, new_info: InfoT) -> None:
        self._info = new_info


    #define a representation of the variant on print readouts
    def __repr__(self) -> str:
        return f"Variant({self._name} - {self._contig.id}:{self._pos} {self._ref}>{self._alt})"

    # define property objects to enforce getters and setters
    contig = property(get_contig, set_contig)
    pos = property(get_pos, set_pos)
    name = property(get_name, set_name)
    ref = property(get_ref, set_ref)
    alt = property(get_alt, set_alt)
    filt = property(get_filt, set_filt)
    qual = property(get_qual, set_qual)
    info = property(get_info, set_info)



# define functions
# define a function to convert simple chromosome IDs (i.e. 1, 2, 3, X, ...)
# to ones that match UCSC (chr1, chr2, chr3, chrX, ...)
def make_ucsc_chrom(contig_name: str) -> str:
    if not contig_name.startswith('chr'):
        return ("chr" + contig_name)
    else:
        return contig_name

# define a function to convert UCSC pattern chromosome IDs (i.e. chr1, chr2, chr3, chrX, ...)
# to the simple ones often found in Broad Institute Genome Assemblies (1, 2, 3, X, ...)
def make_simple_chrom(contig_name: str) -> str:
    if contig_name.startswith('chr'):
        return (contig_name[3:])
    else:
        return contig_name


# define a function to extract core attributes from summary stats file tokens
def extract_core_attributes(tokens : Tokens, indices: Indices) -> Tokens: 
    return tuple(tokens[i] if i != '.' else '.' for i in indices)

# define a function to extract core attributes from summary stats file tokens
def extract_stat_attributes(tokens : Tokens, indices: Indices) -> InfoT: 
    stats_raw = tuple((float(tokens[i]),) if i != '.' else (None,) for i in indices)

    beta: Beta = stats_raw[0]
    beta_se: StdErr = stats_raw[1]
    effect: Effect = (beta, beta_se)
    zscore: ZScore = (compute_zscore(effect) if stats_raw[2] == (None,) else stats_raw[2])
    pval: PValue = (compute_pvalue(zscore) if stats_raw[3] == (None,) else stats_raw[3])
    logp: LogPValue = (compute_logpvalue(pval) if stats_raw[4] == (None,) else stats_raw[4])

    return {
        "BETA": beta,
        "SE": beta_se,
        "Z": zscore,
        "P": pval,
        "LOGP": logp 
    }


# define function to generate a variant object from a set of tokens
def variant_from_tokens(tokens: Tokens, core_ind: Indices, stat_ind: Indices,
                        contigs_dict: Dict[str, Contig], contig_convert: ConvertChoices) -> Variant:
    core_attrs = extract_core_attributes(tokens, core_ind)
    stat_attrs = extract_stat_attributes(tokens, stat_ind)
    
    if contig_convert == 'ucsc': contig = contigs_dict[make_ucsc_chrom(core_attrs[0])]
    elif contig_convert == 'simple': contig = contigs_dict[make_simple_chrom(core_attrs[0])]
    else:
        contig = contigs_dict[core_attrs[0]]
    
    return Variant(
        contig = contig,
        pos = int(core_attrs[1]),
        name= core_attrs[2],
        ref = core_attrs[3],
        alt = core_attrs[4],
        filt='.',
        qual='.',
        info= stat_attrs
    )
