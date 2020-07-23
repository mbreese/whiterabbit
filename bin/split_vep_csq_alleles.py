#!/usr/bin/env python3
# take an VEP annotation VCF file and split the CSQ field by alternative alleles
# output each CSQ set on a separate line for each alt allele
#
# CSQ defintion
# ##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|MANE|TSL|APPRIS|SIFT|PolyPhen|AF|CLIN_SIG|SOMATIC|PHENO|PUBMED|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE">
#

import sys

CSQ_vals = 'Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|MANE|TSL|APPRIS|SIFT|PolyPhen|AF|CLIN_SIG|SOMATIC|PHENO|PUBMED|MOTIF_NAME|MOTIF_POS|HIGH_INF_POS|MOTIF_SCORE_CHANGE'.split('|')


def proc_csq(s):
    ret = {}

    for k, v in zip(CSQ_vals, s.split('|')):
        ret[k] = v
    
    return ret

wrote_header = False

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#':
            sys.stdout.write(line)
            continue
        
        if not wrote_header:
            sys.stdout.write('chrom\tpos\tref\talt\t%s\n' % '\t'.join(CSQ_vals[1:]))
            wrote_header = True

        cols = line.strip().split('\t')


        for alt in cols[4].split(','):
            outs = [cols[0], cols[1], cols[3]]
            outs.append(alt)

            for info_val in cols[7].split(';'):
                if info_val.startswith('CSQ='):
                    
                    best_csq = None

                    for allele_csq in info_val[4:].split(','):
                        csq = proc_csq(allele_csq)
                        if alt == csq['Allele']:
                            if not best_csq:
                                best_csq = csq
                                continue

                            if csq['BIOTYPE'] == 'protein_coding' and best_csq['BIOTYPE'] != 'protein_coding':
                                best_csq = csq
                                continue

                            if csq['IMPACT'] == 'HIGH' and best_csq['IMPACT'] != 'HIGH':
                                best_csq = csq
                                continue

                            if csq['IMPACT'] == 'MODERATE' and best_csq['IMPACT'] != 'MODERATE':
                                best_csq = csq
                                continue

                            if csq['IMPACT'] == 'LOW' and best_csq['IMPACT'] != 'LOW':
                                best_csq = csq
                                continue



                    if best_csq:
                        for k in CSQ_vals[1:]:
                            outs.append(best_csq[k])
                # else:
                #     print("?? %s " % info_val)
            


            sys.stdout.write('%s\n' % '\t'.join(outs))