library(ggplot2)
library(RColorBrewer)

GENOME_FAI<-'data/hg19.fa.fai'
DP_FNAME <- 'out/dp.txt'

pal <- brewer.pal(5,'Set1')



####################
# Setup the genome chromosome position offsets
#####################

genome<-read.table(GENOME_FAI, sep='\t', header=F)[,1:2]
colnames(genome) <- c('chrom', 'size')
rownames(genome) <- genome$chrom

# remove chrM
genome <- genome[genome$chrom != 'chrM',]

genome$chrom <- gsub("chr","",genome$chrom)
genome$chrom <- factor(genome$chrom, levels=as.character(c(1:22,'X', 'Y')))

genome <- genome[order(genome$chrom),]

genome$offset <-0
genome$mid <-0

tmp <- 0
for (i in 1:nrow(genome)) {
  genome[i,]$offset <- tmp
  genome[i,]$mid <- tmp + (genome[i,]$size / 2)
  
  tmp <- tmp + genome[i,]$size
}


####################
# Read the depth data
#####################

df <- read.table(DP_FNAME, sep = '\t', stringsAsFactors = F, comment.char = '#', header = T)
df$logDP <- log2(df$DP)

df$chrom <- factor(df$chrom, levels=as.character(c(1:22,'X', 'Y')))
df$offset <- mapply(function(chrom, pos) { pos + genome[genome$chrom==chrom,]$offset }, as.character(df$chrom), df$pos)



####################
# Setup the shading and chromosome positions for the plot
#####################


xlimits <- c(0, max(genome$offset) + genome[genome$offset == max(genome$offset),]$size)
ylimits <- c(min(df$logDP)-0.5, max(df$logDP) + 0.5)

## Setup shading for each chrom...
shading_x<-c()
shading_y<-c()
shading_group<-c()

seg_x <- c()
seg_y <- c()
seg_yend <- c()

for (i in 1:nrow(genome)) {
  if (i > 0) {
    seg_x <- c(seg_x, genome[i,]$offset)
    seg_y <- c(seg_y, -10)
    seg_yend <- c(seg_yend, ylimits[2])
  }
  if (i %% 2 == 0) {
    shading_x <- c(shading_x, genome[i,]$offset, genome[i,]$offset, genome[i,]$offset+genome[i,]$size, genome[i,]$offset+genome[i,]$size)
    shading_y <- c(shading_y, ylimits[1], ylimits[2], ylimits[2], ylimits[1])
    shading_group <- c(shading_group, rep(as.character(genome[i,]$chrom),4))
  }
}

shading <- data.frame(x=shading_x, y=shading_y, group=shading_group)
chr_seg <- data.frame(x=seg_x, xend<-seg_x, y=seg_y, yend=seg_yend)



####################
# Plot the genome-wide depth to look for CNA
#####################


p <- ggplot(df, aes(x=offset, y=logDP, color=chrom)) + 
  geom_polygon(data=shading, mapping=aes(x=x, y=y, group=group), alpha=0.1, inherit.aes=FALSE) +
  geom_point(size=0.8) + 
  geom_segment(data=chr_seg, mapping=aes(x=x, y=y, xend=xend, yend=yend), color='#000000', size=0.1, inherit.aes=FALSE) +
  scale_color_manual(values=rep(pal,5)) +
  scale_x_continuous(breaks=genome$mid, labels=gsub('chr', '', genome$chrom), minor_breaks=c(genome$offset,genome[nrow(genome),]$offset+genome[nrow(genome),]$size)) +
  coord_cartesian(ylim=ylimits, xlim=xlimits, expand=FALSE) +
  theme_bw() +
  labs(x="", y="log2(DP)") +
  theme(
    legend.position="None"
  )

ggsave('out/full-cna.png', width=12, height=4)

