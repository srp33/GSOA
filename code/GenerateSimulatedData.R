set.seed(1)
random = matrix(rnorm(495000, mean=0, sd=1), nrow=990, ncol=500)

signal1 = matrix(rnorm(2500, mean=0, sd=1), nrow=10, ncol=250)
signal2 = matrix(rnorm(2500, mean=3, sd=1), nrow=10, ncol=250)
signal = cbind(signal1, signal2)

data = rbind(random, signal)

rownames(data) = paste("Gene", 1:1000, sep="")
colnames(data) = paste("Sample", 1:500, sep="")

write.table(data, "Simulated/Data.txt", sep="\t", row.names=T, col.names=NA, quote=F)

classData1 = cbind(colnames(data), c(rep("Class1", 250), rep("Class2", 250)))
classData2 = cbind(colnames(data), c(rep("Class1", 250), rep("Class2", 150), rep("Class3", 100)))
write.table(classData1, "Simulated/Classes2.txt", sep="\t", row.names=F, col.names=F, quote=F)
write.table(classData2, "Simulated/Classes3.txt", sep="\t", row.names=F, col.names=F, quote=F)
