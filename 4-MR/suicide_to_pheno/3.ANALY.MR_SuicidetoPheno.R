library("data.table")
library('dplyr')
library('knitr')
library('TwoSampleMR')
library('MRPRESSO')
library("ggplot2")
options(bitmapType='cairo')
path <-  "**/GWAS_summary_stat/"
path_input <-  "**/suicide_to_pheno/"
path_output <- "**/suicide_to_pheno/MR_all/"
setwd(path_output)

ls.IM=as.data.table(read.csv(paste0(path, 'MR.csv'), header = T))

 for (f in c(1:nrow(ls.IM))){ 
      traitA='suicide'
      traitB= ls.IM$description[f]
      
      ## exposure dat
      exposure_dat=as.data.table(fread(paste0(path_input, "/exposure_data/suicide.exposure_dat"), header=T,colClasses=NULL))
      ## outcome dat
      outcome_dat <- as.data.table(fread(file=paste0(path_input,"/outcome_data/", "outcome_", traitB),sep='\t'))
      
      # Harmonise the exposure and outcome data
      dat <- harmonise_data(exposure_dat, outcome_dat, action= 2)
      
      # calculate MR
      MR=mr(dat = dat)
      if (f==1){
        MRsummary=MR
      }else{
        MRsummary=rbind(MRsummary,MR)
      }
      
      ##  sensitivity analysis
      #--Heterogeneity test--
      het <- mr_heterogeneity(dat)
      if (f==1){
        het.summary=het
      }else{
        het.summary=rbind(het.summary,het)
      }
      # if Q_pval<0.05Using a random effects model
      rad_model <- mr(dat,method_list=c('mr_ivw_mre'))  
      if (f==1){
        rad_model.summary=rad_model
      }else{
        rad_model.summary=rbind(rad_model.summary,rad_model)
      } 
      #--Pleiotropy test--
      pleio <- mr_pleiotropy_test(dat)
      if (f==1){
        pleio.summary=pleio
      }else{
        pleio.summary=rbind(pleio.summary,pleio)
      }
      
}
write.table(MRsummary,file="MRsummary",col.names = T,row.names=F,sep="\t",quot=F)
write.table(het.summary,file="het.summary",col.names = T,row.names=F,sep="\t",quot=F)
write.table(rad_model.summary,file="rad_model.summary",col.names = T,row.names=F,sep="\t",quot=F)
write.table(pleio.summary,file="pleio.summary",col.names = T,row.names=F,sep="\t",quot=F)
# rm(list=ls())