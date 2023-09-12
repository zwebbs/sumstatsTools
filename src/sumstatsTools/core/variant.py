# File Name: variant.py
# Created By: ZW
# Created On: 2023-09-11
# Purpose: defines a data structure for a variant 
#   and its associated summary stats to be used in other tools. 


# library imports 
# -----------------------------------------------------------------------------

from collections import namedtuple
from typing import NamedTuple

# define the variant data type which is the base object in sumstats tools
# -----------------------------------------------------------------------------

# the fields to become attributes in the new Variant type
fields: tuple = ('chrom', 'pos','id','eff_allele', 'other_allele',
                 'beta', 'beta_se','zscore', 'pval','logp')

# create the variant type
Variant: NamedTuple = namedtuple('Variant', fields)


