setwd('~/Downloads') 
library(data.table)
library(dplyr)
df<-read.csv('forR.csv',sep='|')
df$X<-NULL
df$Reviewer.Name<-NULL
df$Reviewer_City<-NULL
df$Rating<-NULL
df$Review.Date<-as.Date(df$Review.Date)
df<-df%>%
    mutate(year=year(df$Review.Date))%>%
    mutate(quarter=quarter(df$Review.Date))%>%
    mutate(month=month(df$Review.Date))
#length(unique(filter(df,year==2018)$Restaurant.name))
#length(unique(filter(df,year==2017)$Restaurant.name))
#length(unique(filter(df,year==2016)$Restaurant.name))
useRst<-filter(df,year==2016)$Restaurant.name
Rst_2018<-filter(df,year==2018 & Restaurant.name %in% useRst)
Rst_2017<-filter(df,year==2017 & Restaurant.name %in% useRst)
Rst_2016<-filter(df,year==2016 & Restaurant.name %in% useRst)
df2<-rbind(rbind(Rst_2018,Rst_2017),Rst_2016)
rm(Rst_2018,Rst_2017, Rst_2016,useRst)

for(i in c(2016,2017,2018)){
    for(j in c(1,2,3,4)){
        d<-df2%>%filter(year==i,quarter==j)
        write.csv(d,file=paste('Year',i,'_Q',j,'.csv',sep = ''),sep="|")
    }
}
