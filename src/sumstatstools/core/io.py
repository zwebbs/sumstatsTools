# File Name: io.py
# Created By: ZW
# Created On: 2023-09-19
# Purpose: defines generic io functions for file and text processing


# library imports
# -----------------------------------------------------------------------------

from itertools import islice
from typing import BinaryIO, Tuple, Union
from .custom_types import Tokens, MapF, BinLinesGenerator, Decoder
from .custom_types import BinLines, Lines


# type aliases
# -----------------------------------------------------------------------------

MaybeLines = Union[Lines,Tuple[None]]

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


# define a function that returns true or false based on whether the line
# starts with the given header token 
def is_header(line: str, startswith: str = "#") -> bool:
    return line.startswith(startswith)


# function definitions
# -----------------------------------------------------------------------------

# define a function that returns a an anonymous callable object for retrieving file lines.
# the generate_file_reader function has a batch size argument to denote how many lines to 
# read into memory at once. a batch size of -1 will allow users to read the entire file 
# at once. 
def generate_file_reader(fobj: BinaryIO, batch_size: int = 1000) -> BinLinesGenerator:
    if batch_size == -1:  # batch size code for reading all lines
        return lambda : tuple(islice(fobj, None))
    else:
        return lambda: tuple(islice(fobj, batch_size))
    

# define a function that decodes binary text lines from sumstats reader
# using the passed map function. allows the user to use traditional map as 
# well as other map functions like multiprocessing.Pool.map  
def decode_lines(binary_lines: BinLines, mapf: MapF, dec: Decoder) -> Lines:    
    return tuple(mapf(dec, binary_lines))


# define a function that filters header lines from a tuple of lines
def filter_header_lines(lines: Lines) -> MaybeLines:
    return tuple(filter(is_header, lines))