
# Part 1. Simple housing model
#
# to implement a simple model to predict home prices for a small real estate transactions
#dataset.
#
#
#Questions
#  Describe your methodology. Why did you pick it?
#  What is the performance of your model? What error metrics did you choose?
#  How would you improve your model?
#  How would you host your model in a production environment to predict values of homes in real-time?

checkPkgs <- function(pkgs) {
    pkg.inst <- installed.packages()
    #    pkgs <- c("sqldf", "data.table","ggplot2")
    have.pkg <- pkgs %in% rownames(pkg.inst)
    
    if(any(!have.pkg)) {
        cat("Some packages need to be installed\n")
        r <- readline("Install necessary packages [y/n]? ")
        if(tolower(r) == "y") {
            need <- pkgs[!have.pkg]
            message("installing packages ",
                    paste(need, collapse = ", "))
            install.packages(need)
        }
    }
}

checkPkgs(c("ggplot2", "rpart","ggplot2"))

setwd("/home/wenfeng/work/Codes/opendoor/")

datafile ="./sacramento_txns.csv"
if(!file.exists(datafile)){
    dataURLcsv<-"https://s3.amazonaws.com/opendoor-problems/sacramento_txns.csv"
    download.file(dataURLcsv, datafile, method="curl")
}
cat(paste("Loading data...\n"))
#csvFile <- "sacramento_txns.csv"

house <- read.csv(datafile, header=TRUE, sep=",")

################################################################################
#
# 1. data cleaning
#  missing value, duplicates, variable range
#
################################################################################
#
dim(house)
colnames(house)

# missing values
sapply(house, function(x) sum(is.na(x)))

# Duplicate record,
duplicateRecords <- house[duplicated(house),]
for (i in 1:dim(duplicateRecords)[1]){
    print(house[house$street==duplicateRecords$street[i],])
}
# remove duplicates, only 982 records left
house <- house[!duplicated(house),]

################################################################################
#
# 2. Features 
# 
# category value
#    "street"    "city"      "zip"       "state" 
#    "beds"      "baths"     "sq__ft" 
#    "type"     
#    "sale_date"
#    "price"
#    "latitude"  "longitude"
#
################################################################################


# address features
cat("\n\n Summary of address features.\n")
summary(house[,c('street','city','zip','state')])

# Correlation Matrix for numerical features
cat(paste("\n\n Correlation Matrix...\n\n"))
round(cor(house[,c("beds","baths","sq__ft","price")]),2)

hist(house$beds)
hist(house$baths)
hist(house$sq__ft, breaks=100) # zero sq_fit room found

plot(house$beds,   house$price)
plot(house$baths,  house$price)
plot(house$sq__ft, house$price)

#
plot(house$latitude, house$longitude)

library(ggplot2)
qplot(price, beds, data=house, facets =.~sale_date)


plot(house[,c("beds","baths","price")])


library(plyr)
houseG <- ddply(house, c("beds"), summarise,
                N    = length(price),
                meanP= mean(price),
                sd   = sd(price),
                se   = sd/sqrt(N))

#impute.mean <- function(x) replace(x, is.na(x), mean(x, na.rm))
ind <- is.na(houseG$se)
houseG[ind,]$se = houseG[ind,]$meanP*0.20 # 0.20 is random assigned

# Standard error of the mean
ggplot(houseG, aes(x=beds, y=meanP, colour=factor(baths))) + 
     geom_errorbar(aes(ymin=meanP-se, ymax=meanP+se), width=.1) +
     geom_line() +
     geom_point()

    
################################################################################
#
# 3. models
#
# starting from linear model
#
################################################################################
#

predEval <- function(data, pred){
    pred[pred<0] <- 0
    return(sqrt(1/length(data)*sum((log(pred +1) - log(data+1))^2)))
}
#
# ceate data partition, here only use training and test.
#  no cross-validataion sample
#

library(caret)
ind <- createDataPartition(y=house$price, p=0.8, list=F)
trainSet <-house[ind,]
testSet <- house[-ind,]

    
house1 <- house[house$sq__ft>0,]
lm1 <- lm(price~ beds + baths, data=house1)
lm2 <- lm(price~ beds + baths+sq__ft, data=house1)
anova(lm1, lm2)

#Since, F is very small, we can reject the null hypothesis at the 5% level  of significance.
# AFter
lm3 <- lm(price~ sq__ft, data=house1)
anova(lm3, lm2)
#The output show the results of the partial F-test. 0.0644, we
#After squared foot has been taken into consideration, 
#the beds and baths do not contribute significant.

predict(lm1, data.frame(beds=2, baths=2), interval="confidence")


#glm


library(caret)
f1 <- formula(log(price+1) ~ beds + baths+sq__ft +zip + type)
gbm <- train(f1, data=trainSet, method="bstTree")

p1 <- prediction(gbm, newdata=testSet)
predEval(testSet$price, p1)



library(randomForest)
rfmodel <- randomForest(f1, data=trainSet)
importance(rfmodel)

pred1 <- predict(rfmodel, newdata=testSet)
pred1 <- exp(pred1)-1
predEval(testSet$price, pred1)
plot(testSet$price, pred1)


library(RWeka)
model1 <- M5P(f1, data=trainSet)
pred1    <- predict(model1, newdata=testSet)
pred1 <- exp(pred1)-1
predEval(testSet$price, pred1)
plot(testSet$price, pred1)


#
#
#  save the model in .RData
#  load and run corresponding predict on the server.
# 
# Some alternatives: yhat, DeployR Open, PMML and more.

save(lm1, file="my_model1.rda")
load("my_model1.rda")
predict(lm1, newdata=newdf)

