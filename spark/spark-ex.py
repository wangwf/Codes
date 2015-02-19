
# coding: utf-8

# # Using SPark + matplotlib + ipython mining pcap file
# 
#  
# **Tasks**
# * read and parse raw log files 
# * read and reshape csv-files
# * spark + pandas
# * spark-mllibs
#     * linear regression  
#     * clustering algorithm
#     * decision tree
#  

# #raw data

# In[1]:

sc # SparkContext


# In[2]:

# creating an RDD (Resilient Distributed dataset)
lines= sc.textFile("../dataLogs/learnDataSet.log")
lines


# In[3]:

#Take a peek at the data.
lines.take(1)   # returns an array


# In[4]:

# lines count
lines.count()  #


# In[9]:

# filter short lines
longlines = lines.filter(lambda line: len(line.split(":"))>10).cache()
longlines.count()


# In[10]:

longlines.take(1)


# In[15]:

#
pageTupe = longlines.flatMap(lambda line: line.split(":")).filter(lambda x: x.find(",")>-1)  #.collect()
pageTupe.take(10)


# In[33]:

# Maximum and Minimum response size
responseSize = pageTupe.filter(lambda x: x.split(",")[0]=="response").map(lambda w:int(w.split(",")[1])).cache()

print "responseSize max, min, count, mean"
responseSize.max(),responseSize.min(),responseSize.count(), int(responseSize.mean())


# In[36]:

# frequently words in this log files
#
import re
def mapper(line):
    words = re.split(",", line)
    return [(w.lower(), 1)for w in words if w.isalpha()]

#lines = sc.textFile("output3_df.txt")
word_freqs = lines.flatMap(mapper).reduceByKey(lambda a,b: a+b).collect()
word_freqs = sorted(word_freqs, key= lambda x: ~x[1])[:10]
word_freqs


# In[38]:

get_ipython().magic(u'pylab inline')
import matplotlib.pyplot as plt

words = [w[0] for w in word_freqs]
y_pos = range(len(word_freqs))
frequency = [w[1] for w in word_freqs]

plt.barh(y_pos, frequency[::-1], align="center", alpha=0.4)
plt.yticks(y_pos, words[::-1])
plt.xlabel("Frequency")
plt.title("Most common words")
#plt.show()


# In[ ]:




# # read pandas- dataframe

# In[349]:

lines = sc.textFile("../dataLogs/output3_df.txt")

lines.distinct().count()


# In[350]:

labels = lines.take(1)[0].split(",")
lst=[labels.index("response"),labels.index("X-Runtime"),labels.index("timeStampStartEnd")]
lst


# In[331]:


lines=lines.filter(lambda line: line.find("response")<0)
words=lines.map(lambda line: line.replace('"', ""))           .map(lambda line: line.replace(", ", "  "))           .map(lambda line: line.replace(" ,", " "))           .map(lambda line: line.split(" "))


# In[354]:

words.count()
#lines.take(1)[0].find("response")


# In[355]:

words.take(1)


# In[356]:

len(lines.take(1)[0].split(","))


# In[356]:




# In[ ]:




# # pandas dataframe to spark

# In[ ]:




# In[123]:

import pandas as pd
dFile = "../dataLogs/output3_df.txt"
DF = pd.DataFrame(pd.read_csv(dFile, header = 0)) #hea


# only continoues columns
labels=[key for key in dict(DF.dtypes) if dict(DF.dtypes)[key] in ['float64', 'int64']]

print labels
for l in ["Content-Length", "Unnamed: 0", "content","headers","cert","response"]:
    labels.remove(l)

#data1=data.iloc[:,[37,17,41]]
data1 = DF.loc[:,["response"]+labels]
data1[:5]


# In[124]:

#data1.drop('cert', axis=1, inplace=True)
#data1.drop("Unnamed: 0", axis=1, inplace=True)
#data1.drop(["Content-Length", "content","header","cert","Unnamed: 0"],axis =1)
data1[:5]


# In[125]:

#for d in data1.iloc[:,[1,2]]:    print d
data1.tail()


# In[126]:

# fill missing value
data1=data1.fillna(0.001)


# In[159]:

#data1["code"]
print data1.drop_duplicates(subset = 'code', inplace = False)
data1.count() #[:5]


# In[178]:

print ["response"]+labels
ll =["response"]+labels
ll[2:3]+ll[4:6]+ll[7:8]+ll[10:]


# #DataFrame subset, only continous features

# In[131]:

#for d in data1.ix[:,:]:    print d[:,:]
#for index, row in data1.iterrows():     print row.values[0:3] #, row[1],row[2]  #row['X-Runtime']

data1.to_csv("test.csv",index=False)


# In[111]:

#data1=data.iloc[:,[37,17,41]]
dataRDD = sc.parallelize(data1)
#parsedData = dataDF.filter(lambda x: x.find("response")!=0).map(parsePoint)
#parsedData.take(2)
dataRDD


# In[375]:

data1[:1]


# In[391]:

from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from numpy import array

data = sc.textFile("test.csv")

# Load and parse the data
def parsePoint(line):
    values = array([float(x) for x in line.split(",")]) #replace(",", " ").split(" ")]
    values2=  array([values[5],values[4], values[10]]) # [values[2], values[4], values[5],values[7],values[10]])
    return LabeledPoint(values[0], values2) # values[1:])

parsedData = data.filter(lambda x: x.find("response")<0).map(parsePoint)


# In[392]:

parsedData.take(2)


# In[393]:

# Build the model
model = LinearRegressionWithSGD.train(parsedData)

# Evaluate the model on training data
valuesAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))


# In[396]:

for d in valuesAndPreds.take(10):
    print d


# In[410]:

zip(*valuesAndPreds.take(5))


# In[416]:

# plot 
plt.xlabel("response")
plt.ylabel("prediction")
plt.scatter(*zip(*valuesAndPreds.collect()))


# In[419]:

plt.xlabel("response")
plt.ylabel("prediction")

fig = plt.subplot(111)
fig.scatter(*zip(*valuesAndPreds.collect()))  #plot(target, prediction, 'bs', target,target, 'r--')
xlim=5000
fig.set_xlim([0,xlim])
fig.set_ylim([0,xlim])
plt.show()


# #Unsupervised Clustering -- Kmean

# In[450]:

from pyspark.mllib.clustering import KMeans
data = sc.textFile("test.csv")
parsedData = data.filter(lambda x: x.find("response")!=0)                 .map(lambda line: array([float(x) for x in line.split(",")]))

# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 2, maxIterations=10,
        runs=10, initializationMode="random")

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))

prediction = parsedData.map(lambda point: clusters.predict(point))


# In[452]:

#[clusters.predict(p) for p in parsedData.take(10)],
prediction.take(10)


# In[438]:

# Visilization 


# In[ ]:




# # decision tree

                
convert csv to libsvm format

 $ python csv2libsvm.py test.csv test_libsvm.data 0 1


                
# In[420]:

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.util import MLUtils

# Load and parse the data file into an RDD of LabeledPoint.
data = MLUtils.loadLibSVMFile(sc,"test_libsvm.data")

# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])


# Train a DecisionTree model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
model = DecisionTree.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                    impurity="variance", maxDepth=5, maxBins=32)

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression tree model:')
print(model.toDebugString())


# In[421]:

#?MLUtils.loadLibSVMFile


# In[422]:

data.take(1)


# In[423]:

labelsAndPredictions.take(1)


# In[424]:

type(labelsAndPredictions.take(1)[0])


# In[425]:

l2=list(labelsAndPredictions.collect())
l2[1][1]


# In[426]:

# 
plt.xlabel("response")
plt.ylabel("prediction")
plt.scatter(*zip(*labelsAndPredictions.collect()))


# In[427]:

plt.xlabel("response")
plt.ylabel("prediction")

fig = plt.subplot(111)
fig.scatter(*zip(*labelsAndPredictions.collect()))  #plot(target, prediction, 'bs', target,target, 'r--')
xlim=5000
fig.set_xlim([0,xlim])
fig.set_ylim([0,xlim])
plt.show()


# #K-mean cluster

# In[428]:

import numpy as np
#from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans


lines = sc.textFile("test.csv")
lines = lines.filter(lambda x: x.find("response")<0)


parsedData = lines.filter(lambda x: x.find("response")<0)                  .map(lambda line: array([float(x) for x in line.split(',')]))


# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 2, maxIterations=10,
        runs=10, initializationMode="random")

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))


#lines.take(2),parsedData.take(1)


# In[453]:

parsedData.take(1),clusters.centers


# In[497]:

prediction = parsedData.map(lambda point: clusters.predict(point))
prediction.take(10)


# In[517]:

x2=parsedData.map(lambda x: [x[0]]+[x[4]]).collect()
type(x2)


# In[511]:

x2[:][1]


# In[518]:

plt.xlabel("response")
plt.ylabel("X-Runtime")
plt.scatter(*zip(*x2),c=prediction.collect())


# In[512]:




# In[430]:


def testKMean(lines, k=2):

#    lines = sc.textFile(sys.argv[1])
    data = lines.map(parseVector)
    model = KMeans.train(data, k)
    print "Final centers: " + str(model.clusterCenters)
    
#testKMean(lines, 2)
#data1= lines.map(parseVector)
#data1.take(1)
lines.take(2)


def mapper(line):
    """
    Mapper that converts an input line to a feature vector
    """    
    feats = line.strip().split(",") 
    # labels must be at the beginning for LRSGD, it's in the end in our data, so 
    # putting it in the right place
    label = feats[len(feats) - 1] 
    feats = feats[: len(feats) - 1]
    feats.insert(0,label)
    features = [ float(feature) for feature in feats ] # need floats
    return np.array(features)

#parsedData = lines.map(mapper)


# In[ ]:



