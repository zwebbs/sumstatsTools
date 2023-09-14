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
from typing import TextIO, Dict, List
from .contigs import Contig
from .variant import Variant


# constants
# -----------------------------------------------------------------------------

headertop = (
    "##fileformat=VCFv4.2",
    "##fileDate={}",
    "##source={}",
    "##reference={}",
    "##doi={}",
    "##phenotype={}")

headerbottom=(
    "##INFO=<ID=BETA,Number=1,Type=Float,Description=\"Effect Size of ALT Variant\">",
    "##INFO=<ID=SE,Number=1,Type=Float,Description=\"Standard Error of BETA\">",
    "##INFO=<ID=Z,Number=1,Type=Float,Description=\"Z-score of ALT Variant\">",
    "##INFO=<ID=P,Number=1,Type=Float,Description=\"P-value of ALT Variant\">",
    "##INFO=<ID=LOGP,Number=1,Type=Float,Description=\"-1*log10(P) of ALT Variant\">",
    "##FILTER=<ID=.,Description=\"Not Provided\">",
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO"
)


# high-level function definitions
# -----------------------------------------------------------------------------

# define write_vcf_header function which takes as input a file object open in
# write mode, as well as a metadata dictionary containing the column mappings
def write_vcf_header(fobj: TextIO, metadata: Dict[str, Dict[str,str]], contigs: List[Contig]) -> None:
    # format the top header string
    studydata: Dict[str,str] = metadata['study']
    program: str = str(Path(sys.argv[0]).stem)
    fmtdtop: str = ("\n".join(headertop).format(date.today(),program,
                                         studydata['genome_build'],
                                         studydata['doi'],
                                         studydata["phenotype"]) + '\n')
    
    # generate the midsection string of the header
    middle: List[str] = [f"##contig=<ID={c.id},length={str(c.length)},assembly={c.assembly}>" for c in contigs]
    fmtdmiddle: str = ('\n'.join(middle) + "\n")
    
    # format the bottom header string
    fmtdbottom: str = ('\n'.join(headerbottom) + '\n')

    # write the header to the file
    fobj.write(fmtdtop)
    fobj.write(fmtdmiddle)
    fobj.write(fmtdbottom)
    return


# define write_vcf_record function which takes a Variant object and writes a line
# to the file specified in the passed file object.
# the fields of the VCF are CHROM POS ID REF ALT QUAL FILTER INFO
def write_vcf_record(var: Variant, fobj: TextIO) -> None:
    fmtd: str = (f"{var.chrom}\t{var.pos}\t{var.id}\t{var.other_allele}\t{var.eff_allele}\t.\t.\t"
                 f"BETA={var.beta};SE={var.beta_se};Z={var.zscore};P={var.pval};LOGP={var.logp}\n")
    fobj.write(fmtd)
    return