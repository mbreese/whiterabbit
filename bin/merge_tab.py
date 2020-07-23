#!/usr/bin/env python3
#
# Merges multiple tab-delimited tab files together
# 
# This assumes there is some set of common keys (chrom, pos, ref, alt) for each record.
# This also assumes that all other columns are uniquely named. If they aren't, then the
# last file included wins.
#

import sys

def usage():
    print("""
Usage: merge_tab.py common_cols output_cols file1.txt file2.txt...

common_cols and output_cols can both be comma-separated lists of column names to include in the output.
By default all common_cols will be included as the first columns in the output.

Alternatively, specific columns can be included from a file like this: file1.txt:col,file2.txt:col, etc...

NOTE: This assumes the files are in consistent order. It does not attempt to re-sort
      or otherwise read the full file into memory. This also assumes that the header/column
      names are the first uncommented line.      

""")
    sys.exit(1)

def error(msg):
    sys.stderr.write('%s\n' % msg)
    sys.exit(1)


def merge_files(fnames, common_cols, output_cols):

    fobjs = []
    falias = []
    headers = []

    for fname in fnames:
        if ':' in fname:
            alias, fname = fname.split(':')
            falias.append(alias)
        else:
            falias.append(fname)

        f = open(fname, 'rt')
        fobjs.append(f)

        line = next(f)
        while line[0] == '#':
            line = next(f)
        
        headers.append(line.strip().split('\t'))

    common_idx = []
    output_idx = []
    first = True

    for common_col in common_cols:
        found = False
        for i,val in enumerate(headers[0]):
            if val ==  common_col:
                common_idx.append((0, i))
                if not first:
                    sys.stdout.write('\t')
                sys.stdout.write(val)
                first = False
                found = True
                break

        if not found:
            error("Missing common column: '%s'" % common_col)

    for output_col in output_cols:
        found = False
        for i, alias in enumerate(falias):
            for j,val in enumerate(headers[i]):
                if val ==  output_col:
                    output_idx.append((i, j))
                    sys.stdout.write('\t%s' % output_col)
                    found = True
                    break
                if '%s:%s' % (alias,val) ==  output_col:
                    output_idx.append((i, j))
                    sys.stdout.write('\t%s' % output_col)
                    found = True
                    break

        if not found:
            error("Missing output column: '%s'" % output_col)


    sys.stdout.write('\n')

    while True:
        try:
            lines = [next(f) for f in fobjs]
            cols = [line.strip().split('\t') for line in lines]

            outs = []
            for i,j in common_idx:
                outs.append(cols[i][j])
            for i,j in output_idx:

                if len(cols[i]) <= j:
                    outs.append('')
                else:
                    outs.append(cols[i][j])

            sys.stdout.write('%s\n' % '\t'.join(outs))

        except StopIteration:
            break

    for fobj in fobjs:
        fobj.close()

    pass

if __name__ == '__main__':
    fnames = []
    common_cols = None
    output_cols = None

    for arg in sys.argv[1:]:
        if not common_cols:
            common_cols = arg.split(',')
        elif not output_cols:
            output_cols = arg.split(',')
        else:
            fnames.append(arg)

    if not fnames or not common_cols or not output_cols:
        usage()

    merge_files(fnames, common_cols, output_cols)
