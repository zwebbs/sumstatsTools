# File Name: custom_types.py
# Created By: ZW
# Created On: 2023-09-19
# Purpose: defines broadly used type aliases for the sumstatstools package


# library imports
# -----------------------------------------------------------------------------

from typing import Tuple, List, Callable, Union, Any
from .contig import Contig
from .variant import Variant

# type aliases
# -----------------------------------------------------------------------------

BinLines = Tuple[bytes,...]
BinLinesGenerator = Callable[[],BinLines]

Tokens = Tuple[str,...]
Lines = Tuple[str,...]
Container = Union[List[Any],Tuple[Any,...]]
MapF = Callable[[Callable[[Any],Any],Container],Any]
Decoder = Callable[[BinLines],Lines]

ContigsT = Tuple[Contig,...]
VariantsT = Tuple[Variant,...]