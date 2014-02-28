resultsFilePath1 = commandArgs()[7]
resultsFilePath2 = commandArgs()[8]
outFilePath = commandArgs()[9]
xlab = commandArgs()[10]
ylab = commandArgs()[11]

results1 = read.table(resultsFilePath1, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F)
results2 = read.table(resultsFilePath2, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F)
results = merge(results1, results2, by=0)
rownames(results) = results[,1]
results = results[,-1]

x = results[,1]
y = results[,7]

#corr = cor(x, y, method="pearson")
rho = cor(x, y, method="spearman")

pdf(outFilePath)
par(mar=c(5.8, 5.6, 0.5, 0.5))
plot(x, y, xlab=xlab, ylab="", main="", pch=20, cex=1.5, xaxt="n", yaxt="n", cex.lab=2, cex.main=2, xlim=c(0.3, 1), ylim=c(0.3, 1))
axis(1, seq(0, 1, 0.05), cex.axis=1.5, lwd.ticks=3.5, tick=T)
axis(2, seq(0, 1, 0.05), cex.axis=1.5, lwd.ticks=2, tick=T, las=1)
title(ylab=ylab, cex.lab=2, mgp=c(4, 1, 0))
box(lwd=3)
#text(0.50, 0.98, paste("Pearson corr. = ", format(corr, digits=3), "\n", "Spearman's rho = ", format(rho, digits=3), sep=""), offset=0, cex=1.5)
text(0.50, 0.98, paste("rho = ", format(rho, digits=3), sep=""), offset=0, cex=1.5)
graphics.off()

#data1 = read.table(dataFilePath1, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F, quote="\"", na.strings=c("NA", "null"))
#notNA = as.logical(apply(data1, 1, function(x) { sum(sapply(x, is.na)) == 0} ))
#data1 = data1[which(notNA),]
#data2 = read.table(dataFilePath2, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F, quote="\"")

#commonGenes = sort(intersect(rownames(data1), rownames(data2)))
#commonSamples = sort(intersect(colnames(data1), colnames(data2)))
#data1 = data1[commonGenes, commonSamples]
#data2 = data2[commonGenes, commonSamples]

#classesData = read.table(classesFilePath, sep="\t", stringsAsFactors=F, header=F, row.names=NULL, check.names=F)
#classesData = classesData[which(classesData[,1]%in%commonSamples),]
#classes = classesData[,2]

#for (pathway in rownames(results)[1:1])
#{
#  geneListFilePath = paste(geneListsDirPath, "/", pathway, sep="")
#  pathwayGenes = scan(geneListFilePath, what=character(0), quiet=TRUE)
#  pathwayGenes = intersect(pathwayGenes, commonGenes)
#
#  #plotHeatmap(pathway, pathwayGenes, data1, "Microarray")
#  #plotHeatmap(pathway, pathwayGenes, log2(data2 + 1), "RNA-Seq")
#
#  corrs = NULL
#  for (gene in pathwayGenes)
#  {
#    corr = cor(as.numeric(data1[gene,]), as.numeric(data2[gene,]), method="spearman")
#    corrs = c(corrs, corr)
#  }
#
#  print(paste("Pearson correlation stats for", pathway))
#  print("Min")
#  print(min(corrs))
#  print("Mean")
#  print(mean(corrs))
#  print("Median")
#  print(median(corrs))
#  print("Max")
#  print(max(corrs))
#}


#corrs = NULL
#for (gene in commonGenes)
#{
#  geneData = cbind(data1[gene,], data2[gene,])
#
#  corr = cor(as.numeric(data1[gene,]), as.numeric(data2[gene,]), method="spearman")
#  corrs = c(corrs, corr)
#}
#
#pdf(paste(outFilePrefix, "GeneCorrelation.pdf", sep=""))
#par(mar=c(4.1, 4.1, 2.2, 0.2))
#hist(corrs, xlab=xlab, ylab=ylab, main="Spearman Correlations - Gene Level", breaks=100)
#print(min(corrs))
#print(mean(corrs))
#print(median(corrs))
#print(max(corrs))
#graphics.off()
