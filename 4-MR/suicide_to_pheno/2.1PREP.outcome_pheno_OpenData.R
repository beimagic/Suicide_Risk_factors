library('dplyr')
library("data.table")
library("TwoSampleMR")
path <- "**/suicide_to_pheno/"
path_input <-  paste0(path, "exposure_data/")
path_output <-  paste0(path, "outcome_data/")
setwd(path_output)

ls.IM=as.data.table(read.csv(paste0(path, 'phenotypes.csv'), header = T))

sui_exp <- as.data.table(fread(paste0(path_input, "suicide.exposure_dat"), header=T, colClasses=NULL))
for (f in c(1:nrow(ls.IM))){
       traitA='suicide'
       traitB= ls.IM$description[f]
       IDs =  ls.IM$UKB_online[f]
       ## outcome dat
       outcome_dat <- extract_outcome_data(
         snps=sui_exp$SNP,
         outcomes=IDs,
         proxies = FALSE,
         maf_threshold = 0.01,
         access_token = NULL
       )
       outcome_dat$outcome=ls.IM$description[f]
       print(dim(outcome_dat))
       write.table(outcome_dat,file=paste0(path_output,"outcome_", traitB),col.names=T,row.names = F,sep="\t",quot=F)
       rm(outcome_dat)
 }
 rm(list=ls())