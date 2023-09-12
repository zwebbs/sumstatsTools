# File Name: sumstatsToVCF.py
# Created By: ZW
# Created On: 2023-09-12
# Purpose: commandline tool for converting flat GWAS summary stats text file
#   to a v4.2 compliant VCF file. the program takes as arguments a metadata json
#   file that describes the column keys in the summary stats file as they correspond
#   to the required field attributes in the VCF, as well as some information on where
#   the summary stats came from for the VCF header 

# library imports
# -----------------------------------------------------------------------------

import argparse
from json import load


# MAIN execution routine
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # build command line parser
    # -------------------------------------------------------------------------

    # program description
    desc = """
            sumstatsToVCF converts a flat GWAS summary stats file to a VCF for
            downstram use. VCF files are better suited for operations
            in bioinformatics pipelines and have s standardized format for cross
            study analysis.
        """
    
    # configure command line parser
    parser = argparse.ArgumentParser(prog="sumstatsToVCF", description=desc)
    parser.add_argument("sumstats_file", type=str, help="summary stats file to convert")
    parser.add_argument("metadata", type=str, help="metadata JSON file")
    parser.add_argument("-o", "--output", type=str, help="name of output vcf", default="out.vcf")

    # parse user arguments
    args = parser.parse_args()


    # read in the metadata json file and create a dictionary
    # -------------------------------------------------------------------------

    with open(args.metadata, 'r') as jobj:
        metadata = load(jobj)





