library(WGCNA)

inFilePattern = commandArgs()[7]
outFilePath = commandArgs()[8]

inFileNamePattern = glob2rx(basename(inFilePattern))
inFilePaths = list.files(path=dirname(inFilePattern), pattern=inFileNamePattern, full.names=TRUE)

readData = function(filePath)
{
  data = as.matrix(read.table(filePath, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F))
  data = data[,-ncol(data)] # ignore the last column

#  rankData = NULL
#  for (i in 1:ncol(data))
#    rankData = cbind(rankData, rank(data[,i]))
#  colnames(rankData) = colnames(data)
rankData = data

  return(rankData)
}

inDataList = list()
for (inFilePath in inFilePaths)
  inDataList[[inFilePath]] = readData(inFilePath)

rankPValueMatrix = NULL

for (i in 1:ncol(inDataList[[inFilePaths[1]]]))
{
  colData = NULL
  for (inFilePath in inFilePaths)
    colData = cbind(colData, inDataList[[inFilePath]][,i])

  rankPValueMatrix = cbind(rankPValueMatrix, rankPvalue(colData)$pValueLowRank)
}

rankPValueMatrix = rankPValueMatrix[order(apply(rankPValueMatrix, 1, mean)),] # sort by average p-value
rownames(rankPValueMatrix) = rownames(inDataList[[inFilePaths[1]]])
colnames(rankPValueMatrix) = colnames(inDataList[[inFilePaths[1]]])

write.table(rankPValueMatrix, outFilePath, sep="\t", quote=F, row.names=TRUE, col.names=NA)
