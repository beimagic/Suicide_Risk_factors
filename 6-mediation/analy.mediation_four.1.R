# This script was used to perform mediation analysis for X - Gray matter(mean) - molecular- suicide attempts
# Bei Zhang 2023

rm(list=ls())
library(lavaan)
library(dplyr)
library(bruceR)
library(lavaanPlot)
path_med <-  "I:/Suicide/Mediation/"
path_output <- "I:/Suicide/Mediation/Results/"
setwd(path_med)

#select different factors
mlist <- c("proteins" ,"bc", "bb", "nmr")
for (k in c(1:4)){
###### basic lists
if (k==1){
  m.ls1=as.data.frame(fread(paste0(path_med,"Med_proteins.csv")))
  mean_1 ="mpr"
}else if (k==2){
  m.ls1=as.data.frame(fread(paste0(path_med,"Med_bc.csv")))
  mean_1 ="mbc"
}else if (k==3){
  m.ls1=as.data.frame(fread(paste0(path_med,"Med_bb.csv")))
  mean_1 ="mbb"
}else if (k==4){
  m.ls1=as.data.frame(fread(paste0(path_med,"Med_nmr.csv")))
  mean_1="mnmr"
}
colnames(m.ls1)[1] <- "eid"

m.ls2=as.data.frame(fread(paste0(path_med,"Med_gm.csv")))
mean_2 ="mgm"
cov.ls= as.data.frame(fread(paste0(path_med,"beh.cov.csv")))

x.ls= as.data.frame(fread(paste0(path_med,"X_factors.csv")))
y.ls= as.data.frame(fread(paste0(path_med,"Y_factor.csv")))

data1 <- merge(y.ls, x.ls, by="eid")
data2 <- merge(m.ls1, m.ls2, by="eid")
data3 <- merge(data1, data2, by="eid")
data <- merge(data3, cov.ls, by="eid")

###### make mediation model list
for (i in c(2:ncol(x.ls))){
  x.n =  colnames(x.ls)[i]
  m1.n = mean_1
  m2.n =  mean_2
  y.n = "SA"
  all.n <- c(x.n, m1.n, m2.n, y.n)
  set.seed(1234)
  
  Data <- data[ , c(x.n, m1.n, m2.n, y.n, "TIV", colnames(cov.ls))]
  colnames(Data)[1:4] <- c("X", "M1", "M2","Y")
  
  if (m1.n=="mgm"){
    m1.model='M1~age+sex+TIV+site'
  }else{
    m1.model='M1~age+sex+site'
  }
 
  if (m2.n=="mgm"){
    m2.model='M2~age+sex+TIV+site'
  }else{
    m2.model='M2~age+sex+site'
  }
   
  model <- paste0('# mediator
                      M1 ~ a1*X
                      M2 ~ a2*X + d21*M1
                      Y ~ b2*M2+b1*M1+c1*X
                      ie := a1*d21*b2
                      total := c1 + (a1*d21*b2) + (a1*b1)+(a2*b2)

                      # X M Y control for age and sex (TIV and Site effects)
                      X ~ age+sex+site
                      Y ~ age+sex+site
                      \n',
                  m1.model,'\n',
                  m2.model,'\n' )
  fit <- sem(model, data = Data, se = "bootstrap", bootstrap = 1000) #用boottrap获得置信区间
  fits=fitMeasures(fit,c('cfi','tli','rmsea','rmsea.ci.lower','rmsea.ci.upper','rmsea.pvalue'))
  para.fits=parameterEstimates(fit, standardized = TRUE, boot.ci.type='perc')
  fits=c((para.fits[nrow(para.fits)-1,5]/para.fits[nrow(para.fits),5]),fits)
  fits=cbind(rbind(all.n,rep(NA,4),rep(NA,4), rep(NA,4), rep(NA,4), rep(NA,4), rep(NA,4), rep(NA,4)),
             para.fits[c((nrow(para.fits)-1):(nrow(para.fits)), 1:6),1:ncol(para.fits)],
             rbind(fits,rep(NA,7),rep(NA,7),rep(NA,7),rep(NA,7),rep(NA,7),rep(NA,7),rep(NA,7)))
  
  if (i==2){
    fits.total=fits
  }else{
    fits.total=rbind(fits.total,fits)
  }
  print(i)
}

colnames(fits.total)[1:4] =c("predictor", "modi1","modi2", "outc")
colnames(fits.total)[18]= "ratio_es"  #indirect(est)/direct(est)
rownames(fits.total)=NULL
if (m1.n =="mgm"){
  write.table(fits.total, paste0(path_output, "X_mgm_", mlist[k], "_suicide2.csv"), sep=',', row.names = F) 
}else{
  write.table(fits.total, paste0(path_output,  "X_", mlist[k],"_mgm_suicide2.csv"), sep=',', row.names = F)
}
}