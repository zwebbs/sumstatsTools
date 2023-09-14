# sumstatsTools: 
## A python package for working with GWAS summary stats files

## Table of Contents


## Tools

### sumstatsToVCF
This tool converts a flat, tabular summary stats file to a VCF which is a standard format accepted by many bioinformatics
tools (e.g. Picard, GATK, bedtools, bcftools, ...). The program has three required inputs: (1) A metadata .json file with the below format. (2) a chromosome sizes file with the below format.  (3) a tabular summary stats file output from GWAS software with descriptive columnwise header. The output vcf filepath can be specified by the `-o, --output` flag. Chromosome conversion from simple representations (e.g. 1, 2, X, ...) to ucsc style representations (chr1, chr2, chrX, ...) and vice-versa can be specified using `--chr-convert [ucsc|simple|none]` with the default being no conversion.


#### The metadata.json file

The metadata file format. a valid JSON file with the following structure:

```json
{
    "study" : {
        "doi" : "<doi of the GWAS if published, else simply '.'>",
        "genome_build" : "<Name of Genome Build for Summary Stats Positions and Chromsomes>",
        "phenotype" : "<GWAS Phenotype>"
    },
    "columns" : {
        "chrom" : "<Summary Stats file column name corresponding to the Chromosome of the Variant>",
        "pos" : "<Summary Stats file column name corresponding to the Position of the Variant>",
        "id" : "<Summary Stats file column name corresponding to the rsids/IDs of the Variant> | null",
        "eff_allele" : "<Summary Stats file column name corresponding to the effect allele of the Variant> | null",
        "other_allele" : "<Summary Stats file column name corresponding to the non affect of the Variant> | null",
        "beta": "<Summary Stats file column name corresponding to the Effect Size of the Variant> | null",
        "beta_se" : "<Summary Stats file column name corresponding to the standard error of the Effect Size> | null",
        "zscore" : "<Summary Stats file column name corresponding to the Z-Score of the Variant> | null",
        "pval" : "<Summary Stats file column name corresponding to the P-Value of the Variant> | null",
        "logp" : "<Summary Stats file column name corresponding to the -1*log10(P-Value) of the Variant> | null"
    }
}
```
A quick note: The fields of a VCF corresponding to alleles are typically __REF__ and __ALT__ because the VCF format arises from a history of tools which were developed to find mutations relative to a reference sequence. In our case, __we encode the effect allele as ALT and the non effect allele as REF__ always, regardless of allele frequency. Therefore the stats we collate in the __INFO__ field always refer to the allele in the __ALT__ column of the VCF.

#### The chrom.sizes file

The chrom.sizes file format:

```text
chr1	249250621
chr2	243199373
chr3	198022430
chr4	191154276
chr5	180915260
chr6	171115067
chr7	159138663
chrX	155270560
<next contig> <next contig size>
```


#### A small example

For a small test case with the following summary stats file _test/test.sumstats.txt_:

```text
chromosome	position	rsids	effect_allele	other_allele	beta	standard_error
1	1000000	rs1248234	A	T	-1.4981799	2.7594772
1	1000010	rs2398543	A	T	-1.7545765  4.0266263
1	1000020	rs3456723	C	G	-0.3782277	3.5170109
1	1000030	rs5793934	G	T	5.1950872	1.9166368
1	1000040	rs3478347	T	C	-2.0332577	1.0444417
2	1000000	rs7428232	C	A	-4.1829822  3.8282066
2	1000010	rs9827332	A	C	-0.1607816	1.3360809
2	1000020	rs2378445	A	G	0.781	1.5558593
2	1000030	rs4309586	G	A	-3.3858142	1.4036133
2	1000040	rs8539254	C	A	2.7742415	2.6992007
X	1000000	rs9453524	T	G	2.8249945	2.9574316
X	1000010	rs1205735	T	C	-0.8429743	2.3346222
X	1000020	rs3428472	A	C	-2.9741986  0.8654375
X	1000030	rs5287323	A	T	-0.2319277	4.0588544
X	1000040	rs9324211	C	A	0.15368150	2.5961632
```

the following chrom sizes file _test/test.hg19.chrom.sizes_:

``` text
chr1	249250621
chr2	243199373
chrX	155270560
```

and the following metadata file _test/test.metadata.json_:

```json
{
    "study" : {
        "doi" : "https://fakedoi.org/10.34.1/natgen/23123",
        "genome_build" : "GRCh37",
        "phenotype" : "Myocardial Infarction"
    },
    "columns" : {
        "chrom" : "chromosome",
        "pos" : "position",
        "id" : "rsids",
        "eff_allele" : "effect_allele",
        "other_allele" : "other_allele",
        "beta": "beta",
        "beta_se" : "standard_error",
        "zscore" : null,
        "pval" : null,
        "logp" : null
    }
}
```

we can process using the following code snippet:


```bash
# run the summary stats to VCF conversion tool
sumstatsToVCF -o test/test.hg19.vcf --chr-convert 'ucsc' \
    test/test.metadata.json \
    test/test.hg19.chrom.sizes \
    test/test.sumstats.txt

# sort the output vcf
bcftools sort test/test.hg19.vcf > test.hg19.sorted.vcf

# block-gzip and tabix index (good practice for large VCFs)
bgzip test/test.hg19.sorted.vcf
tabix test/test.hg19.sorted.vcf.gz

```

if we unzip the output _test/test.hg19.sorted.vcf_ it should look like this:

```text
##fileformat=VCFv4.2
##fileDate=2023-09-13
##source=sumstatsToVCF
##reference=GRCh37
##doi=https://fakedoi.org/10.34.1/natgen/23123
##phenotype=Myocardial Infarction
##contig=<ID=chr1,length=249250621,assembly=GRCh37>
##contig=<ID=chr2,length=243199373,assembly=GRCh37>
##contig=<ID=chrX,length=155270560,assembly=GRCh37>
##INFO=<ID=BETA,Number=1,Type=Float,Description="Effect Size of ALT Variant">
##INFO=<ID=SE,Number=1,Type=Float,Description="Standard Error of BETA">
##INFO=<ID=Z,Number=1,Type=Float,Description="Z-score of ALT Variant">
##INFO=<ID=P,Number=1,Type=Float,Description="P-value of ALT Variant">
##INFO=<ID=LOGP,Number=1,Type=Float,Description="-1*log10(P) of ALT Variant">
##FILTER=<ID=.,Description="Not Provided">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	1000000	rs1248234	T	A	.	.	BETA=-1.4981799;SE=2.7594772;Z=-0.5429216447231381;P=0.5871837524896169;LOGP=0.23122596995459924
chr1	1000010	rs2398543	T	A	.	.	BETA=-1.7545765;SE=4.0266263;Z=-0.43574356527696645;P=0.6630227935669846;LOGP=0.1784715410519311
chr1	1000020	rs3456723	G	C	.	.	BETA=-0.3782277;SE=3.5170109;Z=-0.10754237355363329;P=0.914358710986191;LOGP=0.03888339328175554
chr1	1000030	rs5793934	T	G	.	.	BETA=5.1950872;SE=1.9166368;Z=2.7105225152725856;P=0.006717728750937901;LOGP=2.172777536122394
chr1	1000040	rs3478347	C	T	.	.	BETA=-2.0332577;SE=1.0444417;Z=-1.9467412111178635;P=0.051565768214418606;LOGP=1.2876385078513126
chr2	1000000	rs7428232	A	C	.	.	BETA=-4.1829822;SE=3.8282066;Z=-1.0926740996684974;P=0.27453691551238135;LOGP=0.5613992500284861
chr2	1000010	rs9827332	C	A	.	.	BETA=-0.1607816;SE=1.3360809;Z=-0.12033822203430944;P=0.9042152272910124;LOGP=0.04372818357381362
chr2	1000020	rs2378445	G	A	.	.	BETA=0.781;SE=1.5558593;Z=0.5019734110918641;P=0.6156862244190242;LOGP=0.21064056335789516
chr2	1000030	rs4309586	A	G	.	.	BETA=-3.3858142;SE=1.4036133;Z=-2.412212964924171;P=0.01585601686633198;LOGP=1.7998059008916574
chr2	1000040	rs8539254	A	C	.	.	BETA=2.7742415;SE=2.6992007;Z=1.0278011190497987;P=0.30404338977979695;LOGP=0.5170644341633805
chrX	1000000	rs9453524	G	T	.	.	BETA=2.8249945;SE=2.9574316;Z=0.9552188797874479;P=0.3394670201554175;LOGP=0.4692024118407544
chrX	1000010	rs1205735	C	T	.	.	BETA=-0.8429743;SE=2.3346222;Z=-0.36107525234703924;P=0.7180431928160171;LOGP=0.14384943063590164
chrX	1000020	rs3428472	C	A	.	.	BETA=-2.9741986;SE=0.8654375;Z=-3.4366416985628656;P=0.0005889741820310768;LOGP=3.2299037423048995
chrX	1000030	rs5287323	T	A	.	.	BETA=-0.2319277;SE=4.0588544;Z=-0.057141172642211545;P=0.9544327389582474;LOGP=0.020254671909960578
chrX	1000040	rs9324211	A	C	.	.	BETA=0.15368150;SE=2.5961632;Z=0.05919562375739707;P=0.9527962952677882;LOGP=0.020999940177550656
```

Note that the missing values for Z-Score P-Value, and LogP-value not in the original sumstats file have been computed with the available information from the Beta and Standard Error. If the file contains any of these fields already, we won't overwrite them with our computations.


