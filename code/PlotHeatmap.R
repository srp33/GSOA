suppressPackageStartupMessages(require(gplots))

inFilePath = commandArgs()[7]
excludeLastColumn = commandArgs()[8] == "TRUE"
rounded = commandArgs()[9] == "TRUE"
pValueThreshold = as.numeric(commandArgs()[10])
pathwayFilter = commandArgs()[11]
main = commandArgs()[12]
outFilePath = commandArgs()[13]

selectMatrixRows = function(x, indices)
{
  x2 = as.matrix(x[indices,])
  colnames(x2) = colnames(x)  
  x2
}

jetColors <- function(N)
{
  k <- ceiling(N/4);
  temp.red <- c(rep(0,2*k), 1:k, rep(k,k-1), k:1);
  temp.green <- c(rep(0,k), 1:k, rep(k,k-1), k:1, rep(0,k));
  temp.blue <- c(1:k, rep(k,k-1), k:1, rep(0,2*k));
  temp.rgb <- cbind(temp.red, temp.green, temp.blue);
  delta <- 5*k-1 - N;
  delta <- ceiling(delta/2);
  temp.rgb <- temp.rgb[delta:(delta+N-1),]/k;

  ## assemble everything; last value is returned
  rgb(temp.rgb[,1], temp.rgb[,2], temp.rgb[,3]);
}

data = data.matrix(read.table(inFilePath, sep="\t", header=TRUE, row.names=1, quote="\""))

if (excludeLastColumn)
  data = data[,-(ncol(data))]

rowsToKeep = which(apply(data, 1, function(x) {any(x < pValueThreshold)}))
data = selectMatrixRows(data, rowsToKeep)

rowsToKeep = which(grepl(pathwayFilter, rownames(data)))
data = selectMatrixRows(data, rowsToKeep)

if (nrow(data) < 75)
{
  pdf(outFilePath, width=8.5, height=11)
} else {
  if (nrow(data) < 150)
  {
    pdf(outFilePath, width=8.5, height=22)
  } else {
    pdf(outFilePath, width=8.5, height=33)
  }
}

col = jetColors(20)
col = col[length(col):1]

if (rounded)
{
  col = c(col[1], "lightgray")
  key = FALSE
} else {
  col = col[round(quantile(1:length(col), probs=seq(0, 1, 0.05)))]
  key = TRUE
}

cexRow = 0.7

heatmap.2(data, col=col, dendrogram="both", trace="none", key=key, symkey=FALSE, density.info="none", scale="none", main=main, cexRow=cexRow, labCol=colnames(data), labRow=rownames(data), margin=c(6,25), lmat=rbind(c(4,3),c(2,1)), lwid=c(2,4), lhei=c(2.0,14))

graphics.off()
