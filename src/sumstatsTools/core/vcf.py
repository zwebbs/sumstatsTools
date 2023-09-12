# File Name: vcf.py
# Created By: ZW
# Created On: 2023-09-12
# Purpose: defines functions for writing VCF files including  header 
#   and records. records are written from sumstatsTools.variant Variant objects 

# library imports
# -----------------------------------------------------------------------------
import sys
from datetime import date
from pathlib import Path
from typing import TextIO, Dict


# constants
# -----------------------------------------------------------------------------

header = (
    "##fileformat=VCFv4.2",
    "##fileDate={}",
    "##source={}",
    "##reference={}",
    "##doi={}",
    "##phenotype={}",
    "##INFO=<ID=BETA, Number=1, Type=Float, Description=\"Effect Size of ALT Variant\">",
    "##INFO=<ID=SE, Number=1, Type=Float, Description=\"Standard Error of BETA\">",
    "##INFO=<ID=Z, Number=1, Type=Float, Description=\"Z-score of ALT Variant\">",
    "##INFO=<ID=P, Number=1, Type=Float, Description=\"P-value of ALT Variant\">",
    "##INFO=<ID=LOGP, Number=1, Type=Float, Description=\"-1*log10(P) of ALT Variant\">",
    "##QUAL=<ID=., Number=1, Type=String, Description=\"Not Provided\">",
    "##FILTER=<ID=., Number=1, Type=String, Description=\"Not Provided\">",
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO"
)


# high-level function definitions
# -----------------------------------------------------------------------------

# define write_vcf_header function which takes as input a file object open in
# write mode, as well as a metadata dictionary containing the column mappings
def write_vcf_header(fobj: TextIO, metadata: Dict[str, Dict[str,str]]) -> None:
    # format the header string
    studydata: Dict[str,str] = metadata['study']
    program: str = str(Path(sys.argv[0]).stem)
    fmtd: str = "\n".join(header).format(date.today(),program,
                                         studydata['genome_build'],
                                         studydata['doi'],
                                         studydata["phenotype"])
    # write the header to the file
    fobj.write(fmtd)
    return


# define write_vcf_record function which takes a Variant object and writes a line
# to the file specified in the passed file object.
