# File Name: readers.py
# Created By: ZW
# Created On: 2023-09-14
# Purpose: define file input readers and processers for various text
#   file types like tab delimited summary stats files and vcf files

# library imports
# -----------------------------------------------------------------------------

from itertools import islice
from typing import Tuple, Callable, Union, List, Any, BinaryIO


# type aliases
# -----------------------------------------------------------------------------

Tokens = Tuple[str,...]
Container = Union[List[Any],Tuple[Any,...]]
Map_F = Callable[[Callable[[Any],Any],Container],Any]


# primitive function definitions
# -----------------------------------------------------------------------------

# define decoder functions to convert bytes to strings
def dec_utf8(binary_line: bytes) -> str:
    return binary_line.decode('utf-8')
 
def dec_ascii(binary_line: bytes) -> str:
    return binary_line.decode('ascii')


# define a tokenize function that strips excess whitespace and splits
# a text line based on passed delimiter
def tokenize(line: str, delim: str = '\t') -> Tokens:
    return tuple(line.strip().split())


# define functions that compose the decoders and the tokenizer
def dec_utf8_and_tokenize(binary_line: bytes, delim:str = '\t') -> Tokens:
    return tokenize(dec_utf8(binary_line), delim)

def dec_ascii_and_tokenize(binary_line: bytes, delim: str = '\t') -> Tokens:
    return tokenize(dec_ascii(binary_line), delim)


# function definitions
# -----------------------------------------------------------------------------

# define lines_reader function that takes in a python file object
# and a batch size and returns a callable function for that batch size on the
# passed file. sumstats_reader(..., batch size=1) generates a function which
# returns individual lines (in binary representation) while batch size = 100
# returns 100 lines at a time. outputs need to be decoded ('utf-8) or ('ascii')
def lines_reader(file_object: BinaryIO, batch_size: int = 1) -> Callable[[],Tuple[bytes,...]]:
    return lambda: tuple(islice(file_object, batch_size))


# define a function that decodes binary text lines from sumstats reader
# using the passed map function. allows the user to use traditional map as 
# well as other map functions like multiprocessing.Pool.map  
def decode_lines(binary_lines: Tuple[bytes,...],
                 mapf: Map_F,
                 dec: Callable[[bytes],str]) -> Tuple[str,...]:
    
    return tuple(mapf(dec, binary_lines))


# define a function that tokenizes text lines and removes extra whitespace
# the input is a tuple of lines to process, and the output is a tuple of
# tuples containing tokenized lines. the mapf should be one of: map() or
# multiprocessing.Pool.map(). the tokenizer can be any function that takes
# a string input and returns tokens in a tuple. 
def tokenize_lines(lines: Tuple[str,...],
                   mapf: Map_F,
                   tok: Callable[[str],Tokens] = tokenize) -> Tuple[Tokens,...]:
    
    return tuple(mapf(tok, lines))


# define a function that completes both preprocessing steps for the read binary lines
# by mapping the passed composed dec_*_tokenize function over a batch of lines.    
def preprocess_lines(binary_lines: Tuple[bytes,...],
                     mapf: Map_F,
                     procf: Callable[[bytes],Tokens]) -> Tuple[Tokens,...]:
    
    return tuple(mapf(procf, binary_lines))