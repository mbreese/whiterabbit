#!/usr/bin/env python3
#
# Calculates an percentage of reads supporting ref/alt allele counts
#
# Note: in cases with multiple alt-alleles, the ref + alt values may 
# not be the total reads at a position. For this reason, we also export
# the total reads and this is what is used as the denominator.
#

import sys

ref_idx = -1
alt_idx = -1
total_idx = -1

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#':
            sys.stdout.write(line)
            continue
        cols = line.strip().split('\t')

        if cols[0] == 'chrom':

            for i,v in enumerate(cols):
                if v == 'ref_count':
                    ref_idx = i
                elif v == 'alt_count':
                    alt_idx = i
                elif v == 'total_count':
                    total_idx = i
                    
            if ref_idx == -1 or alt_idx == -1 or total_idx == -1:
                sys.stderr.write('Missing column\n')
                sys.exit(1)

            cols.append('ref_pct')
            cols.append('alt_pct')

            sys.stdout.write('%s\n' % '\t'.join(cols))
            continue

        ref = int(cols[ref_idx])
        alt = int(cols[alt_idx])
        total = int(cols[total_idx])


        cols.append(ref / total)
        cols.append(alt / total)

        sys.stdout.write('%s\n' % '\t'.join([str(x) for x in cols]))

