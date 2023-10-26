library('dplyr')
library("data.table")
library("TwoSampleMR")

path_data <- "I:/Suicide/GWAS_protein/results/"
path <- "I:/Suicide/MR/suicide_to_pheno/"
path_input <-  paste0(path, "exposure_data/")
path_output <-  paste0(path, "outcome_data/")
setwd(path_data)

ls.IM=as.data.table(read.csv(paste0(path_trait, 'phenotypes2.csv'), header = T))

sui_exp <- as.data.table(fread(paste0(path_input, "suicide.exposure_dat"), header=T, colClasses=NULL))
 for (f in c(1:nrow(ls.IM))){  
       traitA='suicide'
       traitB= ls.IM$description[f]
       t2d  = as.data.table(fread(paste0(path_data, "result_GWAS_", traitB, ".chrall.txt"), header=T,colClasses=NULL))
       t2d$phenotype <- traitB
       outcome_dat <- format_data(
         dat=t2d,
         type = "outcome",
         snps = sui_exp$SNP,
         header = TRUE,
         phenotype_col = "phenotype",
         snp_col = "SNP",
         beta_col = "BETA",
         se_col = "SE",
         effect_allele_col = "A1",
         other_allele_col = "REF",
         pval_col = "P",
         chr_col = "CHR",
         pos_col = "POS")
       outcome_dat$outcome=ls.IM$description[f]
       print(dim(outcome_dat))
       write.table(outcome_dat,file=paste0(path_output,"outcome_", traitB),col.names=T,row.names = F,sep="\t",quot=F)
       rm(outcome_dat)
 }
 rm(list=ls())