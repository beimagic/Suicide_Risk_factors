library('dplyr')
library("data.table")
library("TwoSampleMR")

path_input <- "I:/Suicide/PRS/BaseData/"
path_output <- "I:/Suicide/MR/suicide_to_pheno/exposure_data/"
setwd(path_output)

# read GWAS data and get significant SNPs
gwas_summarystat = as.data.table(fread(paste0(path_input, "suicide_noUKB"), header=T,colClasses=NULL))
head(gwas_summarystat)
dim(gwas_summarystat) 

SigniSNP=filter(gwas_summarystat,MAF>0.005,MAF<0.995, P < 5*10^-6)
SigniSNP$beta <- log(SigniSNP$OR)
SigniSNP$Phenotype <- 'suicide'
write.table(SigniSNP,file="./suicide.SigniSNP",col.names=T,row.names = F,sep="\t",quot=F)

# read GWAS significant SNPs and clump
exp_dat <- read_exposure_data(
  filename = paste0(path_output, "suicide.SigniSNP"),
  clump = FALSE,
  sep= "\t",
  snp_col = "SNP",
  beta_col = "beta",
  se_col = "SE",
  effect_allele_col ="A1",
  other_allele_col = "A2",
  eaf_col = "MAF",
  pval_col = "P"
)
head(exp_dat)

exposure_dat <-clump_data(exp_dat,clump_r2=0.001,clump_kb=3000)
dim(exposure_dat)
write.table(exposure_dat,file="./suicide.exposure_dat",col.names=T,row.names = F,sep="\t",quot=F)

rm(list=ls())


