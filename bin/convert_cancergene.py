#!/usr/bin/env python3
#
# Extracts only certain fields from the COSMIC gene list that we care about (symbol, role in cancer, and position)
# It will write the list in sorted (chrom:pos) order (so that it can be TABIX indexed.
#
#

import sys

sym_idx = -1
loc_idx = -1
role_idx = -1

outs = {}

chroms = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X Y'.split()

for chrom in chroms:
    outs[chrom] = []

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#' or not line.strip():
            continue
        cols = line.strip().split('\t')

        if sym_idx == -1:
            for i,v in enumerate(cols):
                if v == 'Gene Symbol':
                    sym_idx = i
                elif v == 'Genome Location':
                    loc_idx = i
                elif v == 'Role in Cancer':
                    role_idx = i

            continue

        if sym_idx == -1 or loc_idx == -1 or role_idx == -1:
            sys.stderr.write('Missing column\n')
            sys.exit(1)

        coord = cols[loc_idx]
        chrom, startend = coord.split(':')

        if startend == '-':
            # skip genes w/o a genome location (TRA, etc)
            continue

        start, end = [int(x) for x in startend.split('-')]

        outs[chrom].append((start, end, cols[sym_idx], cols[role_idx]))


for chrom in chroms:
    for start, end, sym, role in sorted(outs[chrom]):
        sys.stdout.write('%s\t%s\t%s\t%s\t%s\n' % (chrom, start, end, sym, role))

