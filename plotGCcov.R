
# Read in the data
data <- read.table("Surirella_20130407_contig.table", header=T)

# Figure 1
cairo_pdf("test.pdf")
hist(log(data[,13]), breaks = "FD", main = "Surirella_20130407 read coverage", xlab = "Average coverage (log)")
dev.off()

# Figure 2
cairo_pdf("test_2.pdf")
plot(log(sort(data[,13])), sort(data[,3]), xlab = "Average coverage (log)", ylab = "Contig length", main = "Surirella_20130407 read coverage / contig length")
dev.off()



### Tests ###
#
# my_hist <- hist(log(data[,13]), plot=F)
# hist(log(data[,13]), breaks = 10000, main = "Surirella_20130407 contig length", xlab = "Average coverage (log)")
# plot(log(data[,13]),
#
#
#

