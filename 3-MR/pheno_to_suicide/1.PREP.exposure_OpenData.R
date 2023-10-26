library('dplyr')
library("data.table")
library("TwoSampleMR")
library("stringr")
path_input <-  "I:/Suicide/MR/GWAS_summary_stat/"
path_base <- "I:/Suicide/PRS/BaseData/"
path <- "I:/Suicide/MR/pheno_to_suicide/"
path_exposure <- paste0(path, "exposure_data_all/")
path_outcome <- paste0(path, "outcome_data_suicide/")
setwd(path_outcome)

ls.IM=as.data.table(read.csv(paste0(path_input, 'phenotypes.csv'), header = T))

# outcome GWAS
t2d  = as.data.table(fread(paste0(path_base, "suicide_noUKB"), header=T,colClasses=NULL))
head(t2d)
dim(t2d) 
t2d$beta <- log(t2d$OR) # change OR to beta

for (f in c(1:nrow(ls.IM))){
      traitA= ls.IM$description[f]
      traitB='suicide'
      IDs =  ls.IM$UKB_online[f]
      ## exposure dat
      exp_dat <- extract_instruments(outcomes=IDs,clump=TRUE, r2=0.001, kb=3000,p1= 1*10^-5, access_token = NULL)
      exp_dat$exposure = ls.IM$description[f]
      head(exp_dat) #check exposure data
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
rm(list=ls())