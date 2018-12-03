setwd('~/Desktop/Proj')
library(data.table)
library(dplyr)
library(plm)
library(caret)
d=read.csv('final.csv')
r_name=unique(d$Restaurant.name)

getDelta<-function(x){
    d0<-d%>%
        filter(Restaurant.name==r_name[x])%>%
        mutate('last_mkt_shr'=c(1,mkt_shr[1:11]))%>%
        mutate('perc_delta'=mkt_shr/last_mkt_shr)%>%
        mutate('delta'=mkt_shr-last_mkt_shr)
    d0<-d0[2:12,]
}
train<-getDelta(1)
for(x in c(2:length(r_name))){
    train<-rbind(train,getDelta(x))
}
train<-train[c(10,11,2:8)]
hist(train$score_t4)

##standardize
scores<-train[c('score_t0','score_t1','score_t2','score_t3','score_t4')]
others<-train[,c('perc_delta','delta','Restaurant.name','Review.date')]
preprc<-preProcess(scores,method = c('center','scale','YeoJohnson'))
st_scores<-predict(preprc,train[c('score_t0','score_t1','score_t2','score_t3','score_t4')])
train<-cbind(others,st_scores)
hist(train$score_t4)
rm(scores, others, st_scores, preprc, x)

model1<-plm(perc_delta~score_t0+score_t1+score_t2+score_t3+score_t4,
    data=train,
    index=c('Restaurant.name','Review.date'),
    model='within',effect='twoways')
summary(model1)

model2<-plm(delta~score_t0+score_t1+score_t2+score_t3+score_t4,
            data=train,
            index=c('Restaurant.name','Review.date'),
            model='within',effect='twoways')
summary(model2)

######################################################################
#TRY min-max standariazation
train2<-getDelta(1)
for(x in c(2:length(r_name))){
    train2<-rbind(train2,getDelta(x))
}
train2<-train2[c(10,11,2:8)]

scores<-train2[c('score_t0','score_t1','score_t2','score_t3','score_t4')]
others<-train2[,c('perc_delta','delta','Restaurant.name','Review.date')]
preprc<-preProcess(scores,method = c('range'))
st_scores<-predict(preprc,train2[c('score_t0','score_t1','score_t2','score_t3','score_t4')])
train2<-cbind(others,st_scores)
hist(train2$score_t4)
rm(scores, others, st_scores, preprc, x)

model3<-plm(delta~score_t0+score_t1+score_t2+score_t3+score_t4,
            data=train2,
            index=c('Restaurant.name','Review.date'),
            model='within',effect='twoways')
summary(model3)

