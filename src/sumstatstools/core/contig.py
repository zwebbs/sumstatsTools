# File Name: contig.py
# Created By: ZW
# Created On: 2023-09-14
# Purpose: define a contig object that represents a genome scaffold
#   on which variants lie. the contig has a name, a length and 
#   an genome build 

# library imports
# -----------------------------------------------------------------------------

from dataclasses import dataclass


# define objects 
# -----------------------------------------------------------------------------

# define the Contig object 
@ dataclass
class Contig:
    id: str
    length: int
    genome_build: str 
