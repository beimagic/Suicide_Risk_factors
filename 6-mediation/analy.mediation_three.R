# This script was used to perform mediation analysis for X - Gray matter(mean)/White matter/blood- suicide attempts
# Bei Zhang 2023

rm(list=ls())
library(lavaan)
library(dplyr)
library(bruceR)
library(lavaanPlot)
path_med <-  "I:/Suicide/Mediation/"
path_output <- "I:/Suicide/Mediation/Results/"
setwd(path_med)

############################################################################
###  X - Gray matter(mean)/White matter/proteins/blood- suicide attempts  ##
############################################################################
mlist <- c("gm", "wm", "proteins" ,"bc", "bb", "nmr")
 for (k in c(1:6)){
# k=1
###### basic lists
if (k==1){
  m.ls=as.data.frame(fread(paste0(path_med,"Med_gm.csv")))
  mean_f ="mgm"
}else if (k==2){
  m.ls=as.data.frame(fread(paste0(path_med,"Med_wm.csv")))
  mean_f ="mwm"
}else if (k==3){
  m.ls=as.data.frame(fread(paste0(path_med,"Med_proteins.csv")))
  mean_f ="mpr"
}else if (k==4){
  m.ls=as.data.frame(fread(paste0(path_med,"Med_bc.csv")))
  mean_f ="mbc"
}else if (k==5){
  m.ls=as.data.frame(fread(paste0(path_med,"Med_bb.csv")))
  mean_f ="mbb"
}else if (k==6){
  m.ls=as.data.frame(fread(paste0(path_med,"Med_nmr.csv")))
  mean_f ="mnmr"
}

  x.ls= as.data.frame(fread(paste0(path_med,"X_factors.csv")))
  y.ls= as.data.frame(fread(paste0(path_med,"Y_factor.csv")))
  cov.ls= as.data.frame(fread(paste0(path_med,"beh.cov.csv")))
 colnames(m.ls)[1] <- "eid"
 
data1 <- merge(y.ls, x.ls, by="eid")
data2 <- merge(cov.ls, m.ls, by="eid")
data <- merge(data1,data2, by="eid")

###### make mediation model list
for (i in 2:ncol(x.ls)){
      x.n =  colnames(x.ls)[i]
      m.n = mean_f
      y.n = "SA"
      all.n <- c(x.n, m.n, y.n)
      set.seed(1234)
      if (k==1){
        Data <- data[ , c(x.n, m.n, y.n, "TIV", colnames(cov.ls))]
      }else{
        Data <- data[ , c(x.n, m.n, y.n, colnames(cov.ls))] 
      }
      colnames(Data)[1:3] <- c("X", "M", "Y")
      
      if (k==1){
        m.model='M~age+sex+TIV+site'
      }else{
        m.model='M~age+sex+site'
      }
      
      model <- paste0(' # direct effect
                      Y ~ c*X
                      # mediator
                      M ~ a*X
                      Y ~ b*M
                      # total effect
                      med := a*b
                      direct := c
                      total := c + (a*b)

                      # X M Y control for age and sex (TIV and Site effects)
                      X ~ age+sex+site
                      \n',
                      'Y~age+sex+site
                      \n',
                      m.model,'\n'
      )

      fit <- sem(model, data = Data, se = "bootstrap", bootstrap = 1000) #用boottrap获得置信区间
      fits=fitMeasures(fit,c('cfi','tli','rmsea','rmsea.ci.lower','rmsea.ci.upper','rmsea.pvalue'))
      para.fits=parameterEstimates(fit, boot.ci.type = "perc", standardized = TRUE)
      fits=c((para.fits[nrow(para.fits)-2,5]/para.fits[nrow(para.fits),5]),fits,para.fits[3,8])
      fits=cbind(rbind(all.n,rep(NA,3),rep(NA,3), rep(NA,3), rep(NA,3), rep(NA,3)),
                 para.fits[c((nrow(para.fits)-2):(nrow(para.fits)), 1:3),1:ncol(para.fits)],
                 rbind(fits,rep(NA,8),rep(NA,8),rep(NA,8),rep(NA,8),rep(NA,8)))
      
      if (i==2){
            fits.total=fits
      }else{
            fits.total=rbind(fits.total,fits)
      }
     print(i)
}
colnames(fits.total)[1:3] =c("predictor", "modi", "outc")
colnames(fits.total)[17]= "ratio_es"  #indirect(est)/direct(est)
colnames(fits.total)[24]= "pvalue.b"
rownames(fits.total)=NULL
write.table(fits.total, paste0(path_output, "X_", m.n, "_suicide2.csv"), sep=',', row.names = F)
rm(fits.total)
}
tmp.res=fits.total
tmp.res=tmp.res[!is.na(tmp.res$predictor),]
# tmp.res=filter(tmp.res,cfi>=0.9,tli>=0.9,rmsea.pvalue>0.05) #,V8<0.05
tmp.res=filter(tmp.res,cfi>=0.9,tli>=0.9) #,V8<0.05
#拟合优度(GFI)接近1.0、RMSEA接近0、CFI接近1.0表示模型较好地拟合数据。
# write.table(tmp.res, paste0(path_output, "X_", m.n, "_suicide_tep2.csv"), sep=',', row.names = F)
