library('dplyr')
library("data.table")
library("TwoSampleMR")
library("stringr")
path_input <-  "**/"
path_base <- "**/BaseData/"
path <- "**/pheno_to_suicide/"
path_exposure <- paste0(path, "exposure_data_all/")
path_outcome <- paste0(path, "outcome_data_suicide/")
setwd(path_outcome)

ls.IM=as.data.table(read.csv(paste0(path_input, 'phenotypes.csv'), header = T))

# outcome GWAS
t2d  = as.data.table(fread(paste0(path_base, "EUR_noUKB_QC.txt"), header=T,colClasses=NULL))

for (f in c(1:nrow(ls.IM))){
      traitA= ls.IM$description[f]
      traitB='suicide'
    
      ## exposure dat
      exp_dat <- extract_instruments(outcomes=IDs,clump=TRUE, r2=0.01, kb=1000, p1= 5*10^-6, access_token = NULL)
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
      write.table(t2d_out,file=paste0(path_outcome, traitA, "_to_suicide"),col.names=T,row.names = F,sep="\t",quot=F)
}
rm(list=ls())