# File Name: variant.py
# Created By: ZW
# Created On: 2023-09-14
# Purpose: define the variant data class that contains positional information
# on the variant, as well as allelec information, and optionally summary stats


# library imports
# -----------------------------------------------------------------------------

from dataclasses import dataclass
from typing import Union
from .contig import Contig
from .new_old.stats import SummaryStats, complete_summarystats


# type definitions
# -----------------------------------------------------------------------------
Id = Union[str, None]
Qual = Union[str,None] 
Filter = Union[str, None]
Info = Union[str, None]
Stats = Union[SummaryStats, None]

# object definitions
# -----------------------------------------------------------------------------

# define the base Variant dataclass
@dataclass
class Variant:
    chrom: Contig
    pos: int
    ref: str
    alt: str
    id: Id = None
    qual: Qual = None
    filt: Filter = None
    info: Info = None
    stats: Stats = None

    def __post_init__(self) -> None:
        if (self.stats != None):
            self.stats = complete_summarystats(self.stats)