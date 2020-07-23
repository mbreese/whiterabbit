#!/usr/bin/env python3

import requests
import sys
import json
 
server = "http://exac.hms.harvard.edu/"
ext = "/rest/bulk/variant/variant"


variants = {}
variant_key = []

import sys

with open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == '#':
            sys.stdout.write(line)
            continue

        cols = line.strip().split('\t')
        ref = cols[3]
        for alt in cols[4].split(','):
            k = '%s-%s-%s-%s' % (cols[0], cols[1], ref, alt)
            variants[k] = (cols[0], cols[1], ref, alt)

            # store a separate list of keys so that we can return 
            # the results in the same order as input
            variant_key.append(k)

r = requests.post(server+ext, data=json.dumps(variant_key), headers={ "Content-Type" : "application/json"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
outfreq = {}
populations = []

decoded = r.json()
for variant in decoded:
    # if not freq:
    #     print(json.dumps(decoded[variant], indent=2, sort_keys=True))
    # print("%s => %s" % (variant, decoded[variant]["allele_freq"]))

    outfreq[variant] = {}
    if 'allele_freq' in decoded[variant]:
        outfreq[variant]['allele_freq'] = decoded[variant]["allele_freq"]
    else:
        outfreq[variant]['allele_freq'] = ""


    # this keeps order consistent across rows
    if 'pop_acs' in decoded[variant]:
        for k in decoded[variant]["pop_acs"]:
            if not k in populations:
                populations.append(k)

    for k in populations:
        if 'pop_acs' in decoded[variant] and 'pop_ans' in decoded[variant]:
            count = decoded[variant]["pop_acs"][k]
            total = decoded[variant]["pop_ans"][k]

            if total > 0:
                outfreq[variant][k] = count / total
            else:
                outfreq[variant][k] = ''
        else:
            outfreq[variant][k] = ''


#print(outfreq)

# parsed = json.loads(r.content)
# print(json.dumps(parsed, indent=2, sort_keys=True))   


sys.stdout.write('chrom\tpos\tref\talt\texac_freq\tcommon_pop\t%s\n' % '\t'.join(populations))

for k in variant_key:
    outs = list(variants[k])
    outs.append(outfreq[k]['allele_freq'])

    best_pop = ''
    best_pop_af = 0

    for p in populations:
        if outfreq[k][p] and outfreq[k][p] > best_pop_af:
            best_pop = p
            best_pop_af = outfreq[k][p]
    
    outs.append(best_pop)

    for p in populations:
        outs.append(outfreq[k][p])

    sys.stdout.write('%s\n' % '\t'.join([str(x) for x in outs]))