# File Name: liftover.py
# Created By: ZW
# Created On: 2023-09-20
# Purpose: defines functions for liftover between genome assemblies


# library imports
# -----------------------------------------------------------------------------

from copy import deepcopy
from typing import Dict,Union
from liftover import ChainFile
from .contig import Contig
from .variant import Variant


# type aliases
# -----------------------------------------------------------------------------

MaybeVariant = Union[Variant, None]

# function definitions
# -----------------------------------------------------------------------------

# define a function that takes a variant as input and converts it
# using the passed liftover.ChainFile object
def liftover_variant(variant: Variant, chain: ChainFile, target_contigs_dict: Dict[str,Contig]) -> MaybeVariant:
    var_copy = deepcopy(variant)
    varcoords = (var_copy.get_contig().get_id(), var_copy.get_pos())
    newcoords = chain[varcoords[0]][varcoords[1]]
    
    # upon successful liftover, convert to 
    if newcoords != []:
        var_copy.set_contig(target_contigs_dict[newcoords[0][0]])
        var_copy.set_pos(newcoords[0][1])
        return var_copy
    
    else:
        return None
        
