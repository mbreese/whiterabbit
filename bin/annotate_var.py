#!/usr/bin/env python3
#
# Take in a VCF file and annotate if each variant (allow multiple per alt), is a:
#     sub, (single base substitution)
#     del, 
#     ins, 
#     multi (multi-base substitution) -- I don't expect these, but maybe present? 
#                                        Turns out --- yes... ACAA => GCAG (the last line)
#
# Writes out as a tab-delimited file with one line per variant
#

import sys

wrote_header = False

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#':
            sys.stdout.write(line)
            continue

        if not wrote_header:
            sys.stdout.write('chrom\tpos\tref\talt\tvartype\n')
            wrote_header = True

        cols = line.strip().split('\t')
        ref = cols[3]
        for alt in cols[4].split(','):
            outs = [cols[0], cols[1], ref]
            outs.append(alt)

            if len(alt) > len(ref):
                outs.append('ins')
            elif len(alt) < len(ref):
                outs.append('del')
            else:
                diff = 0
                for a,b in zip(alt, ref):
                    if a != b:
                        diff += 1
                
                if diff == 1:
                    outs.append('sub')
                else:
                    outs.append('multi')
        
            sys.stdout.write('%s\n' % '\t'.join(outs))