# File Name: vcf.py
# Created By: ZW
# Created On: 2023-09-19
# Purpose: defines read write operations on Variant objects to
#  and from vcf file formats.

# library imports
# -----------------------------------------------------------------------------

from functools import partial
from typing import Tuple, Dict, Union
from .custom_types import BinLines, MapF, Decoder, Tokens
from .custom_types import VariantsT, ContigsT
from .io import decode_lines, filter_header_lines, tokenize
from .contig import Contig
from .variant import Variant, InfoT


# type aliases
# -----------------------------------------------------------------------------

EmptySet = Tuple[None,...]
MaybeVariantsT = Union[VariantsT,EmptySet]
MaybeContigsT = Union[ContigsT, EmptySet]


# primitive function definitions
# -----------------------------------------------------------------------------

# define a function that takes a string like 'aa=0.5;Effect=0.2,1.1'
# and return a dictionary in the form {'aa' : 0.5 , 'Effect': [0.2, 1.1]}
def vcftext_to_info(token: str) -> InfoT:
    kvpairs = [f.split('=') for f in token.split(';')]
    return {k:tuple(v.split(',')) for k,v in kvpairs}

# define a function that takes an InfoT dictionary object and generates
# an info string. This function inverts the above function
def info_to_vcftext(info: InfoT) -> str:
    return ';'.join(['='.join([k, ','.join(v)]) for k,v in info])


# define a function that takes a properly ordered token set and converts to 
# a variant object. the tokenset order is: chrom, pos, name, ref, alt, filt,
# qual, info
def create_variant(tokens: Tokens, contig_dict: Dict[str,Contig]) -> Variant:
    return Variant(contig=contig_dict[tokens[0]], 
                      pos=int(tokens[1]), 
                      name=tokens[2], 
                      ref=tokens[3], 
                      alt=tokens[4], 
                      filt=tokens[5], 
                      qual=tokens[6], 
                      info=vcftext_to_info(tokens[7]))


# high-level function definitions
# -----------------------------------------------------------------------------

# define a function to process VCF lines from file. the function takes a tuple of bytes
# each of which represents a line in the file. it then decodes the bytes, and returns a
# tuple of variants objects if the lines processed include variants and not solely header
def process_vcf_lines(binary_lines: BinLines, mapf: MapF, dec: Decoder,
                       contig_dict: Dict[str,Contig]) -> MaybeVariantsT:
    dec_lines = decode_lines(binary_lines, mapf, dec)
    filt_lines = filter_header_lines(dec_lines)
    filt_lines_tokens = tuple(mapf(tokenize, filt_lines))
    return tuple(mapf(partial(create_variant, contig_dict=contig_dict), filt_lines_tokens))








