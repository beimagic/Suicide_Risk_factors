library(R.matlab)
library(data.table)
library(dplyr)
library(ggplot2)
library(knitr)
library(readxl)
library(lubridate)
library(stringr)
library(plotrix)
library(lme4)
path <- "**/case_control/"
path_data <- "**/data/"
setwd(path_data)

# load compared individuals
suicide_sample <- as.data.frame(fread(paste0(path_data,"suicide_sample.csv")))

# load phenotypes
all_pheno_data <- as.data.frame(fread(paste0(path_data, "all_data.csv")))

# load pheno list
pheno_list <- as.data.frame(fread(paste0(path_data,"pheno.csv")))

for (i in(1:nrow(pheno_list))){
IDs <- pheno_list$Field_ID[i]
ind <- grep(paste0(IDs, "-"), colnames(all_pheno_data))
#get phenotype value
data <- all_pheno_data[,c("eid", colnames(all_pheno_data)[ind], cov_list)]
colnames(data)[2] <- "value"
data= data[complete.cases(data),]

###calculate statistics based on different value type
pheno_logistic <- glm(group ~ value+ age+ sex+ site,
                      data = data, family = "binomial")
#save statistics
sum_data[sum_data$Field_ID ==IDs, 7:10] <- summary(pheno_logistic)$coef[2,]
write.table(s_data, paste0(path, "sdata/" , "x_", pheno_list$`Field ID`[i], ".csv"), col.names = T, sep=',', row.names = F)
}
colnames(sum_data)[7:10] <- c("beta", "se", "z","p")
write.table(sum_data, paste0(path, "logistic.csv"), col.names = T, sep=',', row.names = F)
