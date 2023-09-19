# File Name: variant.py
# Created By: ZW
# Created On: 2023-09-19
# Purpose: defines the variant object which has a contig, a position, a reference,
#  a name, allele, alternate allele, filter annotation, quality annotation, 
#  and info dictionary.

# library imports
# -----------------------------------------------------------------------------

from typing import Dict, Tuple, Any
from .contig import Contig


# type aliases
# -----------------------------------------------------------------------------

InfoT = Dict[str,Tuple[Any,...]]

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