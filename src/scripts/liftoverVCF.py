# File Name: liftoverVCF.py
# Created By: ZW
# Created On: 2023-09-20
# Purpose: commandline script that reads in a VCF file, lifts over the variant
#  positions, and then writes out a new VCF file in the new assembly.  required 
#  arguments are (1) the input VCF (2) the UCSC chain file (3) the target assembly
#  chrom.sizes file, and (4) the name of the output vcf file. specified using -o
#  or --output flag. Additionally, you may specify a file for variants that cannot
#  be lifted over, using the -u or --unmapped flags, but this is not required. 
#  if no -u/ --unmapped flag and file are given, variants that cannot be mapped 
#  are simply printed to stderr.


# library imports
# -----------------------------------------------------------------------------

import argparse
import time
import sys
import sumstatstools.core.io as io
from liftover import ChainFile
from multiprocessing import Pool
from typing import List,Tuple, TextIO, Union
from sumstatstools.core.contig import Contig
from sumstatstools.core.custom_types import BinLines, Tokens


# define constants
# -----------------------------------------------------------------------------

POOL = Pool()
BATCH_SIZE = 5000

# define functions
# -----------------------------------------------------------------------------

# define a function to preprocess a batch of binary lines
# by decoding and tokenizing
def preprocess_lines(binary_lines: BinLines) -> Tuple[Tokens,...]:
    return tuple(POOL.map(io.dec_utf8_and_tokenize, binary_lines))

# define a function that takes text and writes to either a passed file
# or stderr if the file is None
def write_unmapped(fobj: Union[TextIO, None], text: str) -> None:
    if fobj is not None:
        fobj.write(text)
    else:
        print(text, file=sys.stderr)


# define main() execution routine for script entrypoint
# -----------------------------------------------------------------------------

def main() -> None:
    # start timer for program runtime
    start = time.time()

    # build command line parser
    # -------------------------------------------------------------------------

    # program description
    desc = """
            liftoverVCF converts a VCF file from one genome_assembly to another
            for downstram use. VCF outputs which cannot be mapped can be redirected
            for further inspection.
        """
    
    # configure command line parser
    parser = argparse.ArgumentParser(prog="sumstatsToVCF", description=desc)
    parser.add_argument("input_vcf", type=str, help="vcf file to liftover")
    parser.add_argument("chain_file", type=str, help="UCSC style chain file for genome liftover")
    parser.add_argument("target_chrom_sizes", type=str, help="ucsc style chrom sizes file for new assembly")
    parser.add_argument("-o", "--output", type=str, required=True, help="name of output vcf")
    parser.add_argument("-u", "--unmapped", type=str, help='file for variants to be reported if they cannot be lifted')
    parser.add_argument("-g", "--genome_build", type=str, help="Name or alias of target genome_build")

    # parse user arguments
    args = parser.parse_args()

    
    # open target_chrom_sizes file and build contig dict
    # -------------------------------------------------------------------------
    contigs: List[Contig] = []
    genome_build = args.genome_build if args.genome_build is not None else "UNKOWN"
    with open(args.chrom_sizes, 'rb') as chrobj:
        contig_reader_f = io.generate_file_reader(chrobj, BATCH_SIZE)
        linesbatch = contig_reader_f()
        contigspreproc = preprocess_lines(linesbatch)

        while contigspreproc != ():
            contigsbatch = [Contig(c[0], int(c[1]), genome_build) for c in contigspreproc]
            contigs.extend(contigsbatch)

            linesbatch = contig_reader_f()
            contigspreproc = preprocess_lines(linesbatch)

    contigs_dict = {c.get_id() : c for c in contigs}


    # build liftover chain file 
    # -------------------------------------------------------------------------

    chainfileobj = ChainFile(args.chain_file)


    # open output VCF file for writing and unmapped text file if applicable
    # -------------------------------------------------------------------------

    outvcfobj = open(args.output, 'w')
    if args.unmapped is not None:
        unmappedfobj = open(args.unmapped, 'w')
    else:
        unmappedfobj = None
    

    # open input VCF file for batch processing
    # -------------------------------------------------------------------------

    # liftover variants and write to VCF
    # -------------------------------------------------------------------------

    # close the file connections which are opened during the run
    # -------------------------------------------------------------------------

    outvcfobj.close()
    unmappedfobj.close() if unmappedfobj is not None else None

    # print success message to user
    # -------------------------------------------------------------------------
    
    # stop timer on runtime
    end = time.time()
    print(f"VCF file lifted over: Minutes Elapsed: {(end-start)/60.0}")