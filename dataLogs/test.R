
getwd()

learnFile <- "learnDataSet.log?dl=0"
con <- file(learnFile, open="r")

lines <- readLines(con)
typeof(line)
    
nline=length(line)

#nline =100
for(i in 1:nline){
    if(grepl('error',line[i])){
        data = strsplit(line[i],':')
        # print(paste(length(data[[1]]), i,data[[1]][3]))
      #  print(data[[1]])
      
      # looking error code
      for(j in 1:length(data[[1]])){
          if(grepl('error',data[[1]][j])){
              errorCode = strsplit(data[[1]][j],',')[[1]][2]
              #print(errorCode)
          }
      }     
      #
    }
}

responseSize<-c()
runtime <-c()
i1=0
for(i in 1:nline){
    if(grepl('response',line[i])){
        data = strsplit(line[i],':')
        for(j in 1:length(data[[1]])){
            if(grepl('response',data[[1]][j])){
                rSize = strsplit(data[[1]][j],',')[[1]][2]
                print(rSize)
                i1 =i1+1
                responseSize[i1] <- as.numeric(rSize)
            }
            if(grepl('runtime',data[[1]][j])){
                rSize = strsplit(data[[1]][j],',')[[1]][2]
                print(rSize)
                i1 =i1+1
                responseSize[i1] <- as.numeric(rSize)
            }
            
        }     
    }
}

hist(responseSize, breaks=1000)
hist(responseSize, breaks=100,xlim=c(5e4,25e4),ylim=c(0,10))


hist.data = hist(responseSize, plot=F)
hist.data$counts = log10(hist.data$counts)

dev.new(width=4, height=4)
plot(hist.data, ylab="log10(frequency)", ylim=c(0.5, 50))



## Feature runtime 
responseSize<-c()
runtime <-c()
i1=0
i2=0
for(i in 1:nline){
    if(grepl('response',line[i]) & grepl('Runtime',line[i])){
            data = strsplit(line[i],':')
            for(j in 1:length(data[[1]])){
                if(grepl('response',data[[1]][j])){
                    rSize = strsplit(data[[1]][j],',')[[1]][2]
                    # print(rSize)
                    i1 =i1+1
                    responseSize[i1] <- as.numeric(rSize)
                }
            }
            for(j in 1:length(data[[1]])){
                if(grepl('Runtime',data[[1]][j])){
                    rtime = strsplit(data[[1]][j+1],',')[[1]][1]
                   # print(rtime)
                    i2 =i2+1
                    runtime[i2] <- as.numeric(rtime)
                }
            }  
    }     
}

length(runtime)
length(responseSize)
hist(runtime,breaks=100)

plot(runtime, responseSize[1:419])
