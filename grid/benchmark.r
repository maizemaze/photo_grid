library(ggplot2)
library(magrittr)
library(data.table)
library(tidyr)
setwd("~/Dropbox/James Chen/GRID/Manuscript/Remote Sensing/First Revision/demo")

dt_plot = fread("plot/benchmark_plot.csv") %>%
     gather(metrics, elapse, -plot, -iter) %>% data.table()
dt_size = fread("size/benchmark_size.csv")



ggplot(data=dt_plot, aes(x=plot, y=elapse, group=plot)) + geom_boxplot() + facet_grid(.~metrics)
ggplot(data=dt_size, aes(x=size, y=elapse, group=size)) + geom_boxplot()
