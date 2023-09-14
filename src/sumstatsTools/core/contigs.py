# File Name: contigs.py
# Created By: ZW
# Created On: 2023-09-13
# Purpose: defines a contigs object as well as a function to generate 
#   contigs objects from a ucsc chrom.sizes file

# library imports
# -----------------------------------------------------------------------------

from functools import partial
from typing import Tuple, List, Union, Any, Callable, NamedTuple


# type aliases
# -----------------------------------------------------------------------------

Tokens = Tuple[str,...]
Container = Union[List[Any],Tuple[Any,...]]
Map_F = Callable[[Callable[[Any],Any],Container],Any]

# object definitions
# -----------------------------------------------------------------------------

# define the Contig object which is a named tuple
class Contig(NamedTuple):
    id: str
    length: int
    assembly: str 


# define primitive functions
# -----------------------------------------------------------------------------

# function to take a 2-tuple of tokens (chromosome, length)
# and generate a contig object
def generate_contig(tokens:Tokens, assembly: str) -> Contig:
    return Contig(id=tokens[0], length=int(tokens[1]), assembly=assembly)


# define high-order functions
# -----------------------------------------------------------------------------

# define a function that takes a batch of Tokens from several parsed lines
# and a batch of Contigs objects. can be mapped using map() or multiprocessing.Pool.map()
def generate_contigs(tokens_batch: Tuple[Tokens,...], assembly: str,  mapf: Map_F) -> Tuple[Contig,...]:
    contigs: List[Contig] = mapf(partial(generate_contig,assembly=assembly), tokens_batch)
    return tuple(contigs)
