# File Name: contig.py
# Created By: ZW
# Created On: 2023-09-14
# Purpose: define a contig object that represents a genome scaffold
#   on which variants lie. the contig has a name, a length and 
#   an genome build 


# define objects 
# -----------------------------------------------------------------------------

# define the Contig object 
class Contig:

    # define initial configuration requiring three core attributes to be passed
    def __init__(self,id: str, length: int, genome_build: str) -> None:
        self._id = id
        self._length = length
        self._genome_build = genome_build


    # define getters and setters
    def get_id(self) -> str:
        return self._id
    
    def set_id(self, new_id: str) -> None:
        self._id = new_id

    def get_length(self) -> int:
        return self._length
    
    def set_length(self, new_length: int) -> None:
        self._length = new_length

    def get_genome_build(self) -> str:
        return self._genome_build

    def set_genome_build(self, new_genome_build: str) -> None:
        self._genome_build = new_genome_build


    # define representation of the contig on print readouts
    def __repr__(self) -> str:
        return "Contig(id={self._id}, length={self._length}, genome_build={self._genome_build})"


    # define property objects to enforce getters and setters
    id = property(get_id, set_id)
    length = property(get_length, set_length)
    genome_build = property(get_genome_build, set_genome_build)