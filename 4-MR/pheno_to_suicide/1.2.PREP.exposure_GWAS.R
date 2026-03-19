library('ieugwasr')
library('dplyr')
library("data.table")
library("TwoSampleMR")
path <- "/**/"
path_input <- paste0(path, "GWAS/")
path_base <- paste0(path, "BaseData/")
path_exposure <- paste0(path, "/exposure_data/")
path_outcome <- paste0(path, "outcome_data_suicide/")
setwd(path_input)

ls.IM=as.data.table(read.csv(paste0(path_input, 'phenotypes.csv'), header = T))
t2d  = as.data.table(fread(paste0(path_base, "EUR_noUKB_QC.txt"), header=T,colClasses=NULL))

for (f in c(1:nrow(ls.IM))){
  traitA= ls.IM$description[f]
  traitB='suicide'
  
  ## exposure dat
  gwas_dat = as.data.frame(fread(paste0("result_GWAS_value", f, ".chrall.txt")))
  pheno_dat <- format_data(
    gwas_dat,
    type='exposure',
    snp_col = "SNP",
    beta_col = "BETA",
    se_col = "SE",
    effect_allele_col ="A1",
    other_allele_col = "REF",
    pval_col = "P",
    chr_col = "CHR",
    pos_col = "POS"
  )
  pheno_dat$exposure = ls.IM$description[f]
  pheno_dat_fil <- filter(pheno_dat, pval.exposure <= 5*10^-6)
  
  snp_clump <- ld_clump_local(
    dplyr::tibble(rsid=pheno_dat_fil$SNP,pval=pheno_dat_fil$pval.exposure),
    clump_kb = 1000, clump_r2 = 0.01,clump_p = 1,
    bfile='/**/g1000_eur',
    plink_bin="/**/plink")
  exp_dat <- pheno_dat_fil[which(pheno_dat_fil$SNP %in% snp_clump$rsid),]
  write.table(exp_dat,file=paste0(path_exposure, "Expo_", traitA),col.names=T,row.names = F,sep="\t",quot=F)
  
  # get outcome data
  t2d_out <- format_data(
    dat=t2d,
    type = "outcome",
    snps = exp_dat$SNP,
    header = TRUE,
    phenotype_col = "phenotype",
    snp_col = "SNP",
    beta_col = "BETA",
    se_col = "SE",
    effect_allele_col = "A1",
    other_allele_col = "A2",
    pval_col = "P",
    chr_col = "CHR",
    pos_col = "BP"
  )
  print(dim(t2d_out))
  write.table(t2d_out,file=paste0(path_outcome, traitA, "_to_suicide"),col.names=T,row.names = F,sep="\t",quot=F)
}