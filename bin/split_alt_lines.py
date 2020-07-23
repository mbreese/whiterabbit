#!/usr/bin/env python3
#
# Takes a tab-delimited output file (chrom, pos, ref, alt, ...) and splits the alt values into 
# separate lines if there is more than one. All other columns are unaltered.
#
#

import sys

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#':
            sys.stdout.write(line)
            continue

        cols = line.strip().split('\t')
        if cols[0] == 'chrom':
            sys.stdout.write(line)
            continue

        for alt in cols[3].split(','):
            outs = cols[:]
            outs[3] = alt
            sys.stdout.write('%s\n' % '\t'.join(outs))
            continue
            
