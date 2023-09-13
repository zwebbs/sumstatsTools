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
import sumstatsTools.core.sumstats_ops as ssop
from json import load
from jsonschema import validate
from multiprocessing import Pool
from sumstatsTools.core.vcf import write_vcf_header, write_vcf_record
from sumstatsTools.core.variant import generate_variant_key


# globals
# -----------------------------------------------------------------------------

BATCH_SIZE = 1000
POOL = Pool()

METADATA_SCH = {
    "type" : "object",
    "properties" : {
        "study" : {
            "type" : "object",
            "properties": {
                "doi" : {"type" : "string"},
                "genome_build" : {"type" : "string"},
                "phenotype" : {"type" : "string"}
            },
            "required" : ["doi", "genome_build", "phenotype"],
            "additionalProperties" : True
        },
        "columns" : {
            "type" : "object",
            "properties" : {
                "chrom" : {"type" : ["string", "null"]},
                "pos" : {"type" : ["string", "null"]},
                "id" : {"type" : ["string", "null"]},
                "eff_allele" : {"type" : ["string", "null"]},
                "other_allele" : {"type" : ["string","null"]},
                "beta" : {"type" : ["string","null"]},
                "beta_se" : {"type" : ["string","null"]},
                "zscore" : {"type" : ["string","null"]},
                "pval" : {"type" : ["string","null"]},
                "logp" : {"type" : ["string","null"]}
            },
            "required" : ["chrom", "pos", "id", "eff_allele", "other_allele", "beta", "zscore", "pval", "logp"],
            "additionalProperties" : False
        }
    },
    "required" : ["study", "columns"]
}

# MAIN execution routine
# -----------------------------------------------------------------------------

def main():

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
    parser.add_argument("--chr-convert", type=str, default='none', choices=['none','ucsc','simple'],
                        help='convert chroms to ucsc style [chr1], or simple style [1]')

    # parse user arguments
    args = parser.parse_args()


    # open sumstats file to read, grab header of the file, and prepare batch reader
    # -------------------------------------------------------------------------

    sstobj = open(args.sumstats_file, 'rb')
    sstheader = ssop.dec_utf8_and_tokenize(sstobj.readline())
    sst_reader_f = ssop.sumstats_reader(sstobj, BATCH_SIZE)


    # read metadata file and parse json to dict
    # -------------------------------------------------------------------------

    with open(args.metadata, 'r') as jobj:
        metadata = load(jobj)
        validate(instance=metadata, schema=METADATA_SCH)
        varkey = generate_variant_key(metadata['columns'], sstheader)
    

    # open vcf file to write, create header using information from the metadata
    # -------------------------------------------------------------------------

    vcfobj = open(args.output, 'w')
    write_vcf_header(vcfobj, metadata)


    # read in batches of variants, convert them to Variant objects, and write to vcf
    # -------------------------------------------------------------------------

    # preprocess initial batch, and enter loop. 
    batch = sst_reader_f()
    batchproc = ssop.preprocess_lines(batch, POOL.map, ssop.dec_utf8_and_tokenize)

    # check for sumstats_file EOF
    while batchproc != ():

        # convert to variant objects
        vars = ssop.generate_variants(batchproc, varkey, args.chr_convert, POOL.map)

        # write to vcf (should not be done using multiprocessing)
        [write_vcf_record(var=var, fobj=vcfobj) for var in vars]

        # get next batch and preprocess 
        batch = sst_reader_f()
        batchproc = ssop.preprocess_lines(batch, POOL.map, ssop.dec_utf8_and_tokenize)


    # close open file connections
    # -------------------------------------------------------------------------

    sstobj.close()
    vcfobj.close()



