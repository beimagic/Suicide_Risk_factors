rm(list=ls())
library('dplyr')
library("data.table")
library("TwoSampleMR")
library("stringr")
path_input <-  "I:/Suicide/GWAS/results/"
path_base <- "I:/Suicide/PRS/BaseData/"
path <- "I:/Suicide/MR/pheno_to_suicide/MR_analysis/"
setwd(path)
path_exposure <- paste0(path, "exposure_data_all/")
path_outcome <- paste0(path, "outcome_data_suicide/")
setwd(path_input)

ls.IM=as.data.table(read.csv(paste0(path_input, 'phenotypes2.csv'), header = T))
ls.IM$num <-seq(1:nrow(ls.IM))
 
# outcome GWAS
t2d  = as.data.table(fread(paste0(path_base, "suicide_noUKB"), header=T,colClasses=NULL))
head(t2d)
dim(t2d) 
t2d$beta <- log(t2d$OR) # change OR to beta
head(t2d) 

for (f in c(1:nrow(ls.IM))){
      traitA= ls.IM$description[f]
      traitB='suicide'
      
      ## exposure dat
      pheno_dat <- read_exposure_data(
        filename = paste0("result_GWAS_.", traitA, ".chrall.txt"),
        snp_col = "SNP",
        beta_col = "BETA",
        sep= "\t",
        se_col = "SE",
        effect_allele_col ="REF",
        other_allele_col = "ALT",
        pval_col = "P",
        clump = FALSE
      )
      head(pheno_dat)
      pheno_dat$exposure = ls.IM$description[f]
      pheno_dat <- filter(pheno_dat, pval.exposure <= 1*10^-5)
      print(dim(pheno_dat))
      exp_dat <- clump_data(pheno_dat,clump_r2=0.001,clump_kb=3000)
      print(dim(exp_dat))
      write.table(exp_dat,file=paste0(path_exposure, "Expo_", traitA),col.names=T,row.names = F,sep="\t",quot=F)
      
      # get outcome data
       t2d_out <- format_data(
        dat=t2d,
        type = "outcome",
        snps = exp_dat$SNP,
        header = TRUE,
        phenotype_col = "phenotype",
        snp_col = "SNP",
        beta_col = "beta",
        se_col = "SE",
        effect_allele_col = "A1",
        other_allele_col = "A2",
        pval_col = "P",
        chr_col = "CHR",
        pos_col = "BP"
      )
      print(dim(t2d_out))
      write.table(t2d_out,file=paste0(path_outcome, traitA, "_to_suicide"),col.names=T,row.names = F,sep="\t",quot=F)
      rm(exp_dat)
      rm(t2d_out)
}
