
# Questions
#   I am currently pregnant, and am expecting a baby next year (2015).
#   How much extra should I expect this to cost for my family duirng 2015?
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


library(plyr)
dataG <- ddply(data, c("AGE1X","SEX"), summarise,
                N    = length(TOTEXPY1),
                meanP= mean(TOTEXPY1),
                sd   = sd(TOTEXPY1),
                se   = sd/sqrt(N))



# Standard error of the mean
ggplot(dataG, aes(x=AGE1X, y=meanP, colour=factor(SEX))) + 
    geom_errorbar(aes(ymin=meanP-se, ymax=meanP+se), width=.1) +
    geom_line() +
    geom_point()

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

#
FamilyID <- data[data$DOBYY=="2010",]$DUID
length((FamilyID))
length(unique(FamilyID))
FamilyID <- 

#People died
#Questions:
#    1.) how many Family has a new-born during 2010? 2011?
#    2.) how thesy family's expenditure changes 
#    3.) What about people's annual increament?
#    4.)    

data1 <-data[data$DUID%in%FamilyID,]

dataG <- ddply(data1, c("AGE1X","SEX"), summarise,
                   N    = length(TOTEXPY1),
                   meanP= mean(TOTEXPY2-TOTEXPY1),
                   sd   = sd(TOTEXPY2-TOTEXPY1),
                   se   = sd/sqrt(N))

# Standard error of the mean
ggplot(dataG, aes(x=AGE1X, y=meanP, colour=factor(SEX))) + 
    geom_errorbar(aes(ymin=meanP-se, ymax=meanP+se), width=.1) +
    geom_line() +
    geom_point()
