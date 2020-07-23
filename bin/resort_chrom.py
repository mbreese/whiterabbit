#!/usr/bin/env python3
#
# Resorts a file in natural order for chromosomes (1,2,3,4,5,6,7,8,9,10...,20,21,22,X,Y)
# 
# This reads the entire file in and sorts in memory (warning)
#

import sys

vals = {}

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#':
            sys.stdout.write(line)
            continue

        cols = line.strip().split('\t')
        if cols[0] == 'chrom':
            sys.stdout.write(line)
            continue

        if not cols[0] in vals:
            vals[cols[0]] = []

        vals[cols[0]].append(line)

# this should be done with a proper natural sort, but we can skip that for now
for chrom in '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X Y'.split():
    if chrom in vals:
        for line in vals[chrom]:
            sys.stdout.write(line)

