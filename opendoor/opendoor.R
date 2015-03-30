
cat(paste("Loading data...\n"))
setwd("/Users/wangwf/work/Codes/opendoor/")
csvFile <- "sacramento_txns.csv"
house <- read.csv(csvFile, header=TRUE, sep=",")

