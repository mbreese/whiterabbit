library(ggplot2)
library(viridis)

plot_pct <- function(fname, sample_name) {
    df <- read.table(fname, sep = '\t', stringsAsFactors = F, comment.char = '#', header = T)

    p <- ggplot(df, aes(x=ref_pct, y=alt_pct)) + 
    stat_density_2d(aes(fill = ..density..), geom = "raster", contour = FALSE) +
    geom_density_2d() +
    geom_point(size=0.4, pch=19, alpha=0.5) + 

    scale_x_continuous(expand = c(0, 0)) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_fill_viridis() +
    theme_bw() +
    labs(x="Ref-allele AF", y="Alt-allele AF") +
    theme(
        legend.position="None"
    )

    ggsave(paste0('out/',sample_name,'-pct.png'), width=6, height=4)
}

plot_pct('out/normal.pct.txt', 'normal')
plot_pct('out/vaf5.pct.txt', 'vaf5')