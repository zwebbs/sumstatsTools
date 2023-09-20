# File Name: sumstatsToVCF.py
# Created By: ZW
# Created On: 2023-09-19
# Purpose: defines a script for converting flat summary stats text files to
#  VCF files for downstream processing tasks


# library imports
# -----------------------------------------------------------------------------

import argparse
import time
import sumstatstools.core.io as io
from functools import partial
from json import load
from jsonschema import validate
from multiprocessing import Pool
from typing import Union, List, Tuple, Literal
from sumstatstools.core.custom_types import BinLines, Tokens
from sumstatstools.core.contig import Contig
from sumstatstools.core.vcf import write_vcf_header, write_vcf_record
from sumstatstools.core.variant import variant_from_tokens


# constants
# -----------------------------------------------------------------------------

BATCH_SIZE = 5000  # number of sumstats records to read in at a time
VARIANT_CORE_ATTRS = ['chrom','pos', 'id', 'other_allele', 'eff_allele']
VARIANT_STAT_ATTRS = ['beta', 'beta_se', 'zscore', 'pval', 'logp']

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


# define type aliases
# -----------------------------------------------------------------------------

Indices = List[Union[int,Literal['.']]]


# define functions 
# -----------------------------------------------------------------------------

# define a function to preprocess a batch of binary lines
# by decoding and tokenizing
def preprocess_lines(binary_lines: BinLines) -> Tuple[Tokens,...]:
    return tuple(POOL.map(io.dec_utf8_and_tokenize, binary_lines))


# define main() execution routine for script entrypoint
# -----------------------------------------------------------------------------

def main() -> None:

    # start timer for program runtime
    start = time.time()

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
    parser.add_argument("metadata", type=str, help="metadata JSON file")
    parser.add_argument("chrom_sizes", type=str, help="ucsc style chrom sizes file")
    parser.add_argument("sumstats_file", type=str, help="summary stats file to convert")
    parser.add_argument("-o", "--output", type=str, help="name of output vcf", default="out.vcf")
    parser.add_argument("--chr-convert", type=str, default='none', choices=['none','ucsc','simple'],
                        help='convert chroms to ucsc style [chr1], or simple style [1]')

    # parse user arguments
    args = parser.parse_args()
    

    # open sumstats file to read, grab header of the file, and prepare batch reader
    # -------------------------------------------------------------------------

    sstobj = open(args.sumstats_file, 'rb')
    sstheader = io.dec_utf8_and_tokenize(sstobj.readline())
    sst_reader_f = io.generate_file_reader(sstobj, BATCH_SIZE)

    
    # read metadata file and parse json to dict the validate
    # -------------------------------------------------------------------------

    with open(args.metadata, 'r') as jobj:
        metadata = load(jobj)
        validate(instance=metadata, schema=METADATA_SCH)


    # load contigs from chrom.sizes file and generate contigs dict
    # -------------------------------------------------------------------------
    contigs: List[Contig] = []
    genome_build = metadata["study"]["genome_build"]
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


    # initialize the vcf file object and prepare to write the file
    # -------------------------------------------------------------------------
    vcfobj = open(args.output, 'w')
    write_vcf_header(vcfobj, metadata['study']['genome_build'],
                      metadata['study']['doi'],tuple(contigs_dict.values()))



    # generate variants from summary stats file input and write to vcf
    # -------------------------------------------------------------------------

    # get indices for the core variant attributes
    ind_core: Indices = []
    for attr in VARIANT_CORE_ATTRS:
        try:
            ind=sstheader.index(metadata['columns'][attr])
            ind_core.append(ind)
        
        except ValueError:
            ind_core.append('.') 

    # get indices for the stats attributes that will be converted to an info dict
    ind_stat: Indices = []
    for attr in VARIANT_STAT_ATTRS:
        try:
            ind=sstheader.index(metadata['columns'][attr])
            ind_stat.append(ind)
        
        except ValueError:
            ind_stat.append('.')


    # iterate through batches of lines from the sumstats file. preprocess,tokenize 
    # and convert to variant objects. then write them out to the vcf file.
    
    kwargs = {"core_ind" : ind_core,
              "stat_ind" : ind_stat,
              "contig_convert" : args.chr_convert, 
              "contigs_dict" : contigs_dict}
    
    sumstats_preproc = preprocess_lines(sst_reader_f())
    while sumstats_preproc != ():

        # generate variant objects
        vars = POOL.map(partial(variant_from_tokens, **kwargs),sumstats_preproc)

        # write to VCF
        [write_vcf_record(vcfobj,v) for v in vars]

        # get next batch
        sumstats_preproc = preprocess_lines(sst_reader_f())




    # close persistent file connections
    # -------------------------------------------------------------------------
    sstobj.close()
    vcfobj.close()


    # print success message to user
    # -------------------------------------------------------------------------
    
    # stop timer on runtime
    end = time.time()
    print(f"Summary Stats File Converted to VCF: Minutes Elapsed: {(end-start)/60.0}")
