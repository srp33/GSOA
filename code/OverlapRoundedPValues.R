inFilePattern = commandArgs()[7]
outFilePath = commandArgs()[8]

inFileNamePattern = glob2rx(basename(inFilePattern))
inFilePaths = list.files(path=dirname(inFilePattern), pattern=inFileNamePattern, full.names=TRUE)

readData = function(filePath)
{
  data = as.matrix(read.table(filePath, sep="\t", stringsAsFactors=F, header=T, row.names=1, check.names=F))
}

overlapData = NULL

for (inFilePath in inFilePaths)
{
  inFileData = readData(inFilePath)

  if (is.null(overlapData))
  {
    overlapData = inFileData
  } else {
    inFileData = inFileData[rownames(overlapData),] # make sure matrices are in same order
    overlapData = overlapData & inFileData
  }
}

overlapData = apply(overlapData, 1:2, as.integer)

write.table(overlapData, outFilePath, sep="\t", row.names=T, col.names=NA, quote=F)
