VCF=data/Challenge_data.vcf

all: out/merged.txt \
	out/full-cna.png \
	out/normal-pct.png \
	out/vaf5-pct.png \
	out/cna_gain_genes.txt \
	out/cna_loss_genes.txt

init:
	mkdir out

clean:
	rm -rf out/
	mkdir out

out/merged.txt: out/vartype.txt out/dp.single.txt out/normal.pct.txt out/vaf5.pct.txt out/VEP_function.sorted.txt out/exac_freq.txt bin/merge_tab.py
	bin/merge_tab.py 'chrom,pos,ref,alt' \
		'vartype,IMPACT,Consequence,DP,normal:total_count,vaf5:total_count,normal:ref_count,vaf5:ref_count,normal:alt_count,vaf5:alt_count,normal:ref_pct,vaf5:ref_pct,normal:alt_pct,vaf5:alt_pct,exac_freq,common_pop,SYMBOL,CLIN_SIG' \
		out/vartype.txt out/dp.single.txt normal:out/normal.pct.txt vaf5:out/vaf5.pct.txt out/VEP_function.sorted.txt out/exac_freq.txt \
		> out/merged.txt

out/vartype.txt: $(VCF) bin/annotate_var.py
	bin/annotate_var.py $(VCF) > out/vartype.txt

out/exac_freq.txt: $(VCF) bin/exac_api.py
	bin/exac_api.py data/Challenge_data.vcf > out/exac_freq.txt

out/dp.txt: $(VCF)
	ngsutilsj vcf-export --info 'DP' $(VCF) > out/dp.txt

out/dp.single.txt: out/dp.txt bin/split_alt_lines.py
	bin/split_alt_lines.py out/dp.txt > out/dp.single.txt

out/full-cna.png: out/dp.txt bin/cna.R
	R --vanilla < bin/cna.R

out/normal.counts.txt: $(VCF)
	ngsutilsj vcf-tocount --sample normal --total --use-ro-ao $(VCF) > out/normal.counts.txt

out/vaf5.counts.txt: $(VCF)
	ngsutilsj vcf-tocount --sample vaf5 --total --use-ro-ao $(VCF) > out/vaf5.counts.txt

out/normal.pct.txt: out/normal.counts.txt bin/calc_pct.py
	bin/calc_pct.py out/normal.counts.txt > out/normal.pct.txt

out/vaf5.pct.txt: out/vaf5.counts.txt bin/calc_pct.py
	bin/calc_pct.py out/vaf5.counts.txt > out/vaf5.pct.txt

out/normal-pct.png out/vaf5-pct.png: out/normal.pct.txt out/vaf5.pct.txt
	R --vanilla < bin/plot_af.R

external/cancer_gene_census.txt: external/cancer_gene_census.csv
	tabl csv2tab external/cancer_gene_census.csv > external/cancer_gene_census.txt

external/cancer_gene_census.bed.bgz: external/cancer_gene_census.txt bin/convert_cancergene.py
	bin/convert_cancergene.py external/cancer_gene_census.txt | bgzip > external/cancer_gene_census.bed.bgz
	
external/cancer_gene_census.bed.bgz.tbi: external/cancer_gene_census.bed.bgz
	tabix -p bed external/cancer_gene_census.bed.bgz

# Range taken by eye from CNA plot
out/cna_gain_genes.txt: external/cancer_gene_census.bed.bgz.tbi
	tabix external/cancer_gene_census.bed.bgz 1:145273302-152286254 > out/cna_gain_genes.txt

# Range taken by eye from CNA plot
out/cna_loss_genes.txt: external/cancer_gene_census.bed.bgz.tbi
	tabix external/cancer_gene_census.bed.bgz 6:29910801-31324144 > out/cna_loss_genes.txt


out/VEP_function.txt: data/VEP_annotations.vcf bin/split_vep_csq_alleles.py
	bin/split_vep_csq_alleles.py data/VEP_annotations.vcf > out/VEP_function.txt

out/VEP_function.sorted.txt: out/VEP_function.txt bin/resort_chrom.py
	bin/resort_chrom.py out/VEP_function.txt > out/VEP_function.sorted.txt


.PHONY: init clean all
