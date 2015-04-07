
# Questions
#   I am currently pregnant, and am expecting a baby next year (2015).
#   How much extra should I expect this to cost for my family duirng 2015?
#
# AGE, Sex, Family size, number-of-children, number-of-elder, Faminly Total income
# annual increasement ： inflate
#
#
# Region: R
#   REGIONY1    CENSUS REGION AS OF 12/31/10
#   REGIONY2	CENSUS REGION AS OF 12/31/11
#
#
data <- read.csv("./2010-longitudinal.csv", sep=",")
classes <- sapply( data, class)
classes
#data <- read.csv("./2010-longitudinal.csv", header=TRUE, sep=",", colClasses=classes) 
dim(data)

length(unique(data$DUPERSID))
length(unique(data$DUID))

unique(data$SEX)

range(data$AGE1X)

range(data$TOTEXPY1)
range(data$TOTEXPY2)
plot(data$TOTEXPY2,data$TOTEXPY1)


# Pregnant
#filter(data)
pregantWomen <- data[data$PREGNT1==1|data$PREGNT2==1|data$PREGNT3==1|data$PREGNT4==1|data$PREGNT5==1,]
newbabies <- data[data$DOBYY==2010|data$DOBYY==2011,]
pregantWomen <- pregantWomen[pregantWomen$DUID %in% newbabies$DUID,]
hist(pregantWomen$AGE1X,breaks=52,ylim=c(-2,50))


sum(data10$DUPERSID %in% d$DUPERSID)
sum(data10$DUPERSID %in% d$DUPERSID)

#Alternative, multiple -women in a house
d <- data[data$DUID%in%newbabies$DUID&data$SEX==2&data$AGE1X>16,]
hist(d$AGE1X,breaks=82,xlim=c(-2,80))

# DUID + PID = DUPERSID
#((newbabies$DUID*1000+newbabies$PID==newbabies$DUPERSID)

#sum( (newbabies$DUID*1000+newbabies$MOPID1X) %in% pregantWomen$DUPERSID)
d <- data[data$DUPERSID %in%c(newbabies$DUID*1000+newbabies$MOPID5X),]
hist(d$AGE1X,breaks=82,xlim=c(-2,80))


library(plyr)
dataSEX1 <- ddply(pregantWomen, c("AGE1X","SEX"), summarise,
                  N    = length(TOTEXPY1),
                  meanEXP1= mean(TOTEXPY1),
                  sd1   = sd(TOTEXPY1),
                  se1   = sd1/sqrt(N),
                  N2    = length(TOTEXPY2),                
                  meanEXP2= mean(TOTEXPY2),
                  sd2   = sd(TOTEXPY2),
                  se2   = sd2/sqrt(N2))

#plot1<-
ggplot(dataSEX1, aes(x=AGE1X, y=meanEXP1, colour=factor(SEX), ymax=max(meanEXP1))) + 
    geom_errorbar(aes(ymin=meanEXP1-se1, ymax=meanEXP1+se1), width=.1) +
    geom_line(aes(y=meanEXP1), colour="green")+    
    geom_line(aes(y=meanEXP2), colour="blue")+
    geom_point(position=pd)




#Age and Sex dependence
library(plyr)
dataSEX1 <- ddply(data, c("AGE1X","SEX"), summarise,
                N    = length(TOTEXPY1),
                meanEXP1= mean(TOTEXPY1),
                sd1   = sd(TOTEXPY1),
                se1   = sd1/sqrt(N),
                N2    = length(TOTEXPY2),                
                meanEXP2= mean(TOTEXPY2),
                sd2   = sd(TOTEXPY2),
                se2   = sd2/sqrt(N2))

# Standard error of the mean
#par(mfrwo=c(2,1))  #
library(grid)
library(gridExtra)
pd <- position_dodge(0.1)
plot1<-ggplot(dataSEX1, aes(x=AGE1X, y=meanEXP1, colour=factor(SEX),ymax=max(meanEXP1))) + 
    geom_errorbar(aes(ymin=meanEXP1-se1, ymax=meanEXP1+se1), width=.1) +
    geom_line() +
    geom_point(position=pd)

plot2<-ggplot(dataSEX1, aes(x=AGE1X, y=meanEXP2, colour=factor(SEX),ymax=max(meanEXP2))) + 
    geom_errorbar(aes(ymin=meanEXP2-se2, ymax=meanEXP2+se2), width=.1) +
    geom_line() +
    geom_point()

grid.arrange(plot1,plot2,ncol=1,main="EXPENDITURE Male vs Female")

# Difference M/F 2010
d1<- dataSEX1[dataSEX1$SEX==2,]$meanEXP1 - dataSEX1[dataSEX1$SEX==1,]$meanEXP1
mean(d1[27:33])
d2<- dataSEX1[dataSEX1$SEX==2,]$meanEXP2 - dataSEX1[dataSEX1$SEX==1,]$meanEXP2
mean(d2[23:33])

plot(d1[20:40],xaxt="n",xlab="AGE1X", type="l",ylab="EXPENDITUR 2010",col="blue")
lines(0:20,d2[20:40],col="green")
axis(1, at=0:20, labels=20:40)

#
avgPregnant = mean(d1[26:35])  # averger 1883.

#
# Family cost
hist(data$FAMSZE1)

library(plyr)
dataG <- ddply(data, c("AGE1X","SEX"), summarise,
               N    = length(TOTEXPY1),
               meanP= mean(TOTEXPY2-TOTEXPY1),
               sd   = sd(TOTEXPY2-TOTEXPY1),
               se   = sd/sqrt(N))

# Standard error of the mean
ggplot(dataG, aes(x=AGE1X, y=meanP, colour=factor(SEX))) + 
    geom_errorbar(aes(ymin=meanP-se, ymax=meanP+se), width=.1) +
    geom_line() +
    geom_point()

#
# averge medical E
mean(data$TOTEXPY2)-mean(data$TOTEXPY1)



# Family-ID, Family-size, has-pregant, TOTEXPY1, TOTEXPY2, 
head(data[,grep("^AGE", names(data))])

#how to identify preganent women
#Find home with age
library(sqldf)

#Family ID with baby born at 2010
sum(data$DOBYY==2010)
sum(data$DOBYY==2011)

sum(data$AGE1X==0)

#
# YEARIND: 1 b
sum(data$YEARIND==1)  # person in both 2010 and 2011
sum(data$YEARIND==2)  # person only in 2010
sum(data$YEARIND==3)  # person only in 2011

#
table(data$DOBYY==2011,data$YEARIND==3)
#
data[data$YEARIND==3&data$DOBYY!=2011,]$DOBYY

#FAMSY1 : Family size at 2010
hist(data$FAMSY1)
hist(data$FAMSY2-data$FAMSY1, breaks=20)
#
# Family has newborn 2010
FamilyID10 <- data[data$DOBYY=="2010",]$DUID
length((FamilyID10))
length(unique(FamilyID10))
#FamilyID <- 

#Family has new born 2011
FamilyID11 <- data[data$DOBYY=="2011",]$DUID
length((FamilyID11))
length(unique(FamilyID11))

#Two family number overlap
sum(FamilyID10 %in% FamilyID11)
FamilyBoth10100 <- FamilyID11[FamilyID11 %in% FamilyID10]

#People died
#Questions:
#    1.) how many Family has a new-born during 2010? 2011?
#    2.) how thesy family's expenditure changes 
#    3.) What about people's annual increament?
#    4.)    


# All Family, including pregnant and non-pregant,
FamEXP <- ddply(data, c("DUID"), summarise,
                  FAMTOTEXPY1= sum(TOTEXPY1),
                  FAMTOTEXPY2= sum(TOTEXPY2))
#                   Diff = (TOTEXPY2-TOTEXPY1))

hist(FamEXP$FAMTOTEXPY2-FamEXP$FAMTOTEXPY1, breaks=100)
mean(FamEXP$FAMTOTEXPY2-FamEXP$FAMTOTEXPY1)
# increase about $66

#Military
sum(data11$MILITARY)
data10 <-data[data$DUID%in%FamilyID10,]
data11 <-data[data$DUID%in%FamilyID11,]


FamEXP10 <- ddply(data10, c("DUID"), summarise,
                   FAMTOTEXPY1= sum(TOTEXPY1),
                   FAMTOTEXPY2= sum(TOTEXPY2))
#                   Diff = (TOTEXPY2-TOTEXPY1))

hist(FamEXP10$FAMTOTEXPY2-FamEXP10$FAMTOTEXPY1, breaks=100)
mean(FamEXP10$FAMTOTEXPY2-FamEXP10$FAMTOTEXPY1)
# had baby 2010, 2011 decrease about $10,682


#
#
#
FamEXP11 <- ddply(data11, c("DUID"), summarise,
                  FAMTOTEXPY1= mean(TOTEXPY1),
                  FAMTOTEXPY2= mean(TOTEXPY2))

hist(FamEXP11$FAMTOTEXPY2-FamEXP11$FAMTOTEXPY1, breaks=100)
mean(FamEXP11$FAMTOTEXPY2-FamEXP11$FAMTOTEXPY1)
# have newborn 2011, 2011 increase about $10052



## number-of-child, number-of-elder
hist(data10$AGE1X)

# Health Care Expenditures for Uncomplicated Pregnancies
# http://meps.ahrq.gov/mepsweb/data_files/publications/rf27/rf27.pdf
# http://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp
#https://www.healthdata.gov

#Some family have newborn both 2010 and 2011

# Entered survey after beginning of panel (mainly births; also includes persons 
# who had no initial chance of selection who moved into a MEPS sample household) (0=no, 1=yes)

sum(data10$ENTRSRVY)
sum(data11$ENTRSRVY)

#Moved out of the country
sum(data10$LEFTUS)
sum(data11$LEFTUS)

sum(data10$ALL5RDS==0)
# illness, Diabete
# DSDIA3: 
#DSDIA3  DCS:DIABETES DIAGNSS BY HLTH PROF 10
#DSDIA5	DCS:DIABETES DIAGNSS BY HLTH PROF 11
#DSDIET3	DCS:TREAT DIABETES W/DIET MODIFICATN 10
#DSDIET5	DCS:TREAT DIABETES W/DIET MODIFICATN 11
table(data10$DSDIA3,data10$DSDIA5)
table(data10$DSDIA3,data10$DSDIET3)

#CHang jobs

# Died
sum(data10$DIED==1)
sum(data11$DIED==1)  # one person died 


unique(data11$INST)
unique(data11$INST)


#Family total income
hist(data10$FAMINCY1,breaks=100)
hist(data11$FAMINCY1,breaks=100)


table(data11$PREGNT4)

#
#
#
data11$ageGroup<-cut(data11$AGE1X, br=c(-2,18,60,100),labels=c("kid","adults","elder"))
FamData <- ddply(data11, c("DUID"), summarise,
                  nKids= sum(ageGroup=='kid'),
                  nAdults= sum(ageGroup=='adults'),
                  nElders= sum(ageGroup=='elders'),
                  FAMTOTEXPY1= sum(TOTEXPY1),
                  FAMTOTEXPY2= sum(TOTEXPY2),
                  FAMSY1  = length(FAMSY1),
                  FAMINCY1 = FAMINCY1[1],
                  REGIONY1 = REGIONY1[1])

FamData$FAMEXPInc <- FamData$FAMTOTEXPY2 -FamData$FAMTOTEXPY1
head(FamData[, c("nKids","nAdults","nElders")])


# merge, program
FamData<-merge(FamData, pregantWomen[,c("DUID","AGE1X")],by="DUID")

#
predEva <- function(data, pred){
    meanD <- mean(data)
    return(sqrt(1/length(data) * sum((pred  - data )^2)))
#    return( sum((pred  - mean(data) )^2)/ sum( (data - mean(data))^2) )
}


library(caret)
ind <- createDataPartition(y=FamData$FAMEXPInc, p=0.6, list=F)
trainSet <- FamData[ind,]
testSet  <- FamData[-ind,]

f1 <- formula(FAMEXPInc ~ nKids+FAMSY1+ FAMINCY1 + AGE1X + REGIONY1+ I(FAMINCY1^2) + I(FAMSY1^2) )
#lm1 <- lm(f1, data=trainSet)
library(randomForest)
rfmodel1 <- randomForest(f1, data=trainSet, importance=TRUE, ntree=5000)
importance(rfmodel1)

xylimits =c(0,30000)
p1 <- predict(rfmodel1, newdata=trainSet) #trainSet)
predEva(trainSet$FAMEXPInc, p1)
plot(trainSet$FAMEXPInc, p1, xlim=xylimits, ylim=xylimits, ylab="predicted Expenditure")
abline(0,1,col="blue")

p1 <- predict(rfmodel1, newdata=testSet) #trainSet)
predEva(testSet$FAMEXPInc, p1)
plot(testSet$FAMEXPInc, p1, xlim=xylimits, ylim=xylimits, ylab="predicted Expenditure")
abline(0,1,col="blue")


#p1 <- predict(lm1, newdata=testSet) #trainSet)

#p1 <- round(exp(p1) -1)

predEva(testSet$FAMEXPInc, p1)
plot(testSet$FAMEXPInc, p1, xlim=c(0,15000), ylim=c(0,15000))
abline(0,1,col="blue")

    
#
