dataFilePath1 = commandArgs()[7]
dataFilePath2 = commandArgs()[8]
outFilePath = commandArgs()[9]
xlab = commandArgs()[10]
ylab = commandArgs()[11]

data1 = read.table(dataFilePath1, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F, quote="\"", na.strings=c("NA", "null"))
notNA = as.logical(apply(data1, 1, function(x) { sum(sapply(x, is.na)) == 0} ))
data1 = data1[which(notNA),]
data2 = read.table(dataFilePath2, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F, quote="\"")

print(data1[1:5,1:5])
print(data2[1:5,1:5])

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
