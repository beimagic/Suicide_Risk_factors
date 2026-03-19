rm(list=ls())
library(lavaan)
library(dplyr)
library(bruceR)
library(lavaanPlot)
path_med <-  "**/Mediation/"
path_output <- "**/Results/"
setwd(path_med)

mlist <- c("gm", "wm", "proteins" ,"bc", "bb", "nmr")
 for (k in c(1:6)){
###### basic lists
m.ls=as.data.frame(fread(paste0(path_med, mlist[k], ".csv")))
mean_f = mlist[k]

###### make mediation model list
for (i in 2:ncol(x.ls)){
      x.n =  colnames(x.ls)[i]
      m.n = mean_f
      y.n = "SA"
      all.n <- c(x.n, m.n, y.n)
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
      if (i==2){
            fits.total=fits
      }else{
            fits.total=rbind(fits.total,fits)
      }
     print(i)
}
write.table(fits.total, paste0(path_output, "X_", m.n, "_suicide.csv"), sep=',', row.names = F)
rm(fits.total)
}