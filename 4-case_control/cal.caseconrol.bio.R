# This script was used to perform mediation analysis for case-control for behavioral analysis
# Bei Zhang 2023

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
path <- "I:/Suicide/case_control/"
path_data <- "I:/Suicide/case_control/biological_data/"
path_input <- "I:/Suicide/case_control/data/"
setwd(path_data)

# load compared individuals
suicide_case <- as.data.frame(fread(paste0(path_input,"suicide_indi.csv")))
suicide_con <- as.data.frame(fread(paste0(path_input,"suicide_con.csv")))
suicide_sample <- rbind(suicide_case, suicide_con)

# load phenotypes
all_pheno_data <- as.data.frame(fread(paste0(path_data, "all_data.csv")))
cov <- as.data.frame(fread(paste0(path_data, "cov.csv")))

# load pheno list
pheno_list <- as.data.frame(fread(paste0(path_data,"pheno.csv")))

for (i in(1:nrow(pheno_list))){
IDs <- pheno_list$`Field ID`[i]
ind <- grep(paste0(IDs, "-"), colnames(all_pheno_data))
#get phenotype value
data <- pheno_data_cat[,c("eid", "group", "age", "sex",  "site", colnames(all_pheno_data)[ind])]
colnames(data)[6] <- "value"
data= data[complete.cases(data),]

###calculate statistics based on different value type
pheno_logistic <- glm(group ~ value+age+ sex+ site,
                      data = data, family = "binomial")

# save number of comparision
sum_data[sum_data$`Field ID`==IDs, ]$N_case <- nrow(data[data$group==1,])
sum_data[sum_data$`Field ID`==IDs, ]$N_control <- nrow(data[data$group==0,])
#save statistics
sum_data[sum_data$`Field ID`==IDs, 7:10] <- summary(pheno_logistic)$coef[2,]
write.table(s_data, paste0(path, "sdata/" , "x_", pheno_list$`Field ID`[i], ".csv"), col.names = T, sep=',', row.names = F)
rm(pheno_logistic)
rm(data)
}
colnames(sum_data)[7:10] <- c("beta", "se", "z","p")
sum_data$OR <- round(exp(sum_data$beta),3)
sum_data$lower<-round(exp(sum_data$beta-sum_data$se*1.96),3) 
sum_data$upper<-round(exp(sum_data$beta+sum_data$se*1.96),3) 
write.table(sum_data, paste0(path, "logistic.csv"), col.names = T, sep=',', row.names = F)
