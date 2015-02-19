
# coding: utf-8

# # spark-mongo
# 
# * read data from mongodb to spark
# * write data to mongodb from spark
# 
# SPark + matplotlib + ipython mining pcap

# In[ ]:




# In[1]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt 
import mpld3
mpld3.enable_notebook()


# In[2]:

import pymongo

#
# Connect to MongoDB server
#
def get_db(host="localhost", port=27017, username=None, password=None, db="dataLogs"):
    """ A util for making a connection to mongo """
    from pymongo import MongoClient
    
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

def get_coll(host="localhost", port=27017, username=None, password=None, db="dataLogs",collection="logs"):
    db=get_db(host, port, username, password, db)
    return db[collection]


logs = get_coll('localhost', 27017, None, None,"dataLogs", "logs")
test = get_coll('localhost', 27017, None, None,"dataLogs", "test")


# In[2]:




# In[2]:




# In[3]:

iter=logs.find({"response.headers.content-length":{"$exists":True}},{"_id":0,"response.headers.content-length":1})
for item in iter[:10]: #.count()
    print item
#type(iter)


# #Categorical Features

# In[4]:

#
# turn categorical-text into numerical value
#

categoricalFeatures=["X-Frame-Options","X-Xss-Protection","X-Content-Type-Options","X-Ua-Compatible",
            "X-Xhr-Current-Location",
            "Content-Type","Cache-Control",
            "Server","httpversion","port","scheme","http","path","host", "Connection",
            "ip","Referer","code",
            "Accept-Encoding","Accept-Language",
            "method",
            "msg",
            "address"]

#    featuresSize=["error","response","headers","content","request"]
featuresHeaders=["X-Frame-Options","X-Xss-Protection","X-Content-Type-Options","X-Ua-Compatible",
               "X-Xhr-Current-Location","Content-Type","Etag","Cache-Control",
               "X-Request-Id",  #"X-Runtime",
               "Server","Date",
               "Content-Length", "connection","Set-Cookie"]
featuresHeaders = [f.lower() for f in featuresHeaders]
    
#featuresContent=["content"]
    
featuresRequest=["httpversion", "address","client_conn",  #"requestcount",
                 "error","port",
                    "scheme","path","host", "header",#"content",
                    "method",
                  #  "ssl_setup_timestatmp","timestamp_end","timestamp_start", "tcp_setup_timestamp"
                    "ip"] #,"cookie"]

#featuresRequestHeaders =["host","connection", "accept", "user-agent"]

categoricalFeatures = [ "response.headers."+f for f in featuresHeaders]
categoricalFeatures +=   ["request."+ f for f in featuresRequest]

def categoricalToNumberical(dbColl, fields):
    for f in fields:
        fID=f+"ID"
        vals=dbColl.distinct(f)
        
        if len(vals)<2: continue

        for i,v in enumerate(vals):
#            print f,v,i
            dbColl.update({f:v}, {"$set":{fID: int(i+1) }}, upsert=True, multi=True)

categoricalToNumberical(logs, categoricalFeatures)
categoricalToNumberical(test, categoricalFeatures)

#categoricalFeatures


# In[5]:

#


# In[6]:

logs.update({"response.headers.content-type":"text/css"}, {"$set":{"response.headers.content-typeID": 3 }}, True, True)
iter=logs.find({"response.headers.content-type":"text/css"},{"_id":0, "response.headers.content-type":1,"response.headers.content-typeID":1})

for item in iter: print item


# # RDD

# In[7]:

# 
# Read sc.newAPIHadoopRDD()
# sc.parallelize()
#
def read_mongo(collection, query={}, projection={"_id":0},host='localhost',no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Make a query to the specific DB and Collection
    cursor = collection.find(query, projection)

    # Expand the cursor and construct the DataFrame
#    df = pd.DataFrame(list(cursor))
    df = sc.parallelize(list(cursor))

    # Delete the _id
#    if no_id:       del df['_id']

    return df



# In[8]:


df=read_mongo(logs)
#df_test = read_mongo(test)
type(df)


# In[9]:

#  data =sc.parallelize(df)

df.take(1)


# In[10]:

numericalFeatures =['size.response', 'request.requestcount', 'response.headers.x-runtime', 'request.timestamp_diff'] #'timestamp_end', 'timestamp_start' ]

proj ={"_id": 0}#{"_id":0}

#for l in numericalFeatures:    proj[l] = 1 #{'$exists':True}
categoricalFeaturesID=[l+"ID" for l in categoricalFeatures]

for l in numericalFeatures+categoricalFeaturesID:
    proj[l] =1

#proj['timestampStartEnd'] ={ '$add' : [ '$timestamp_end', '$timestamp_start' ] }
proj["contentLeakage"]=1

print proj
df=read_mongo(logs,query={}, projection=proj)
#df.map(lambda x: x.get("pathID")).collect()


# In[11]:

l=df.take(2)
type(l[0])
#l#["request.methodID"]
#categoricalFeaturesID


# In[12]:

df.take(2)


# #Linear Regression

# In[13]:

from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD

# Load and parse the data

features = numericalFeatures + categoricalFeatures

def parsePoint(line):
#    values=[line.get(f) or 0)  for f in features]
    values=[]
    values.append( line["size"].get("response") or 0)
    values.append( line["response"]["headers"].get("x-runtime") or 0)
#    values.append( line["response"]["headers"].get("content-typeID") or 0)
#    values.append( line["request"].get("methodID") or 0)
#    values.append( line["request"].get("msgID") or 0)
#    values.append( line["request"].get("pathID") or 0)
    values.append( line["request"].get("timestamp_diff") or 0)
#    values.append( line["request"].get("requestcount") or 0)
#    values.append( line.get("contentLeakage") or 0)

    return LabeledPoint(values[0], values[1:]) # values[1:])

parsedData = df.map(parsePoint)


# In[14]:

df.map(lambda line: line["request"]).take(1)


# In[15]:

parsedData.take(10)


# In[16]:

# Build the model
model = LinearRegressionWithSGD.train(parsedData)

# Evaluate the model on training data
valuesAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))


# In[17]:

valuesAndPreds.take(10)


# In[18]:

# plot 
plt.xlabel("response")
plt.ylabel("prediction")
plt.scatter(*zip(*valuesAndPreds.collect()))


# In[18]:




# # decision Tree

# In[19]:

'''
# Load and parse the data file into an RDD of LabeledPoint.
from pyspark.mllib.util import MLUtils
data = MLUtils.loadLibSVMFile(sc,"test_libsvm.data")
data.take(1)[0].label,data.take(1)[0].features
'''


# In[20]:

from numpy import array
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.util import MLUtils

#df.map(lambda x: len(x)).collect()
#features =["response", "X-Runtime", "timestampStartEnd","Content-TypeID","methodID","pathID", "msgID","codeID","contentMatch"]
features = numericalFeatures + categoricalFeatures



def parsePoint(line):
#    values=[line.get(f) or 0)  for f in features]
    values=[]
    values.append( line["size"].get("response") or 0)
    values.append( line["response"]["headers"].get("x-runtime") or 0)
    values.append( line["response"]["headers"].get("content-typeID") or 0)
    values.append( line["request"].get("methodID") or 0)
    values.append( line["request"].get("msgID") or 0)
    values.append( line["request"].get("pathID") or 0)
    values.append( line["request"].get("timestamp_diff") or 0)
    values.append( line["request"].get("requestcount") or 0)
    values.append( line.get("contentLeakage") or 0)

    return values
#    return LabeledPoint(values[0], values[1:]) # values[1:])

#parsedData = df.map(parsePoint)

#d2=parsedData
#d2=df.map(lambda x: [x.get(f) or 0 for i,f in enumerate(features)])

def parsedVector(line):
    length =len(line[1:])
    v = zip(*[ (i,x) for i,x in enumerate(line[1:])])
    sv1 = Vectors.sparse(length, v[0], v[1])

    return LabeledPoint(line[0], sv1) #, list(v[1])))
    
    

d2=df.map(parsePoint).map(parsedVector)

d2.take(2)


# In[21]:

from pyspark.mllib.util import MLUtils

dataOutput="libsvm_data.txt"
import os.path
import shutil
if os.path.exists(dataOutput):
    shutil.rmtree(dataOutput)#os.rmdir(dataOutput)
    print dataOutput

MLUtils.saveAsLibSVMFile(d2,"libsvm_data.txt")


# In[22]:

for i,x in enumerate(features): print i,x


# In[23]:


# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = d2.randomSplit([0.7, 0.3])

# Train a DecisionTree model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
model = DecisionTree.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                    impurity="variance", maxDepth=6, maxBins=12)

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression tree model:')
print(model.toDebugString())


# In[24]:

# 
plt.xlabel("response")
plt.ylabel("prediction")
plt.scatter(*zip(*labelsAndPredictions.collect()))


# In[24]:




# # Random Forest

# In[25]:

from pyspark.mllib.tree import RandomForest

# Train a Random Forest
#  Empty categoricalFeaturesInfo indicates all features are continuous.
model = RandomForest.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                    numTrees=3, featureSubsetStrategy="auto",
                                    impurity="variance", maxDepth=4, maxBins=32)

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression tree model:')
#print(model.toDebugString())

plt.figure
plt.xlabel("response")
plt.ylabel("prediction")
plt.scatter(*zip(*labelsAndPredictions.collect()))


# In[25]:




# In[25]:




# # Gradient Boosted Trees

# In[26]:

from pyspark.mllib.tree import RandomForest


# In[26]:




# #Clustering

# In[27]:



proj={"size.response":1,"request.pathID":1,"contentLeakage":1}
print proj

df=read_mongo(logs,query={}, projection=proj)
df_test = read_mongo(test, query={}, projection=proj)

#(trainingData, testData) = d2.randomSplit([0.7, 0.3])
#df.count(),df_test.count()
df2 = df + df_test
df2.count()

(trainingData, testData) = df2.randomSplit([0.7, 0.3])


# In[28]:

trainingData.take(1)


# In[29]:

def parsePoint(line):
#    values=[line.get(f) or 0)  for f in features]
    values=[]
    values.append( line["size"].get("response") or 0)
    values.append( line["request"].get("pathID") or 0)
#    values.append( line["request"].get("path") or 0)
#    values.append( line.get("contentLeakage") or 0)
    return np.array(values)
#    return LabeledPoint(values[0], values[1:]) # values[1:])

parsedData = trainingData.map(parsePoint)
parsedData.take(10)


# In[30]:

from pyspark.mllib.clustering import KMeans
from numpy import array
from math import sqrt

# Load and parse the data
#data = sc.textFile(dataDir+"data/mllib/kmeans_data.txt")
#parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))

# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 2, maxIterations=10,
        runs=10, initializationMode="random")

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))


# In[31]:

clusters.centers


# In[32]:

import matplotlib.pylab as plt

#plt.figure()
import pandas as pd

df = pd.DataFrame(trainingData.collect())
df[:5]


# In[32]:




# In[33]:


from math import log 
pathIDs   = [ p.get('pathID')  for p in df["request"] ]
response  = [ log(p.get('response') or 1) for p in df["size"]  ]


plt.scatter(response, pathIDs, c=df["contentLeakage"])

#pathIDs
#for p in df["request"]:    print type(p),p['pathID']


# In[33]:




# In[34]:

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes

proj={"contentLeakage":1,
      "size.response":1,"request.pathID":1,
      "response.headers.x-runtime":1,
      "request.timestamp_diff":1
      }
print proj

df=read_mongo(logs,query={}) #, projection=proj)
df_test = read_mongo(test, query={}) #, projection=proj)

#(trainingData, testData) = d2.randomSplit([0.7, 0.3])
#df.count(),df_test.count()
df2 = df + df_test
df2.count()

(trainingData, testData) = df2.randomSplit([0.7, 0.3])


# In[35]:

trainingData.take(2)


# In[36]:

def parsePoint(line):
#    values=[line.get(f) or 0)  for f in features]
    values=[]

    values.append( line.get("contentLeakage") or 0)
    values.append( line["size"].get("response") or 0)
    values.append( line["response"]["headers"].get("x-runtime") or 0)
    values.append( line["response"]["headers"].get("content-typeID") or 0)
    values.append( line["request"].get("methodID") or 0)
    values.append( line["request"].get("msgID") or 0)
    values.append( line["request"].get("pathID") or 0)
    values.append( line["request"].get("timestamp_diff") or 0)
#    values.append( line["request"].get("requestcount") or 0)
    return LabeledPoint(values[0], values[1:]) # values[1:])



parsedData = trainingData.map(parsePoint)
parsedDataT = testData.map(parsePoint)


# In[37]:

parsedData.take(2)


# In[38]:

parsedData.take(1)[0]


# In[39]:

# Train a naive Bayes model.
model = NaiveBayes.train(parsedData, 1.0)

# Make prediction.



def confusionMat(parsedData):
    pred = parsedData.map( lambda p: model.predict(p.features) ).collect() #parsedData.values)
    meas  =  parsedData.map(lambda p: p.label ).collect()
    
    res=[0]*4
    for i in range(len(meas)):
        if meas[i] ==0 and  pred[i]==0: # TT
                res[0] +=1
        elif meas[i] ==0 and  pred[i]==1: # 
                res[1] +=1
        elif meas[i] ==1 and  pred[i]==0:  # False-positive
                res[2] +=1
        else:
                res[3] +=1

    return np.reshape(res, (-1,2))
    
mat=confusionMat(parsedData)
mat


# In[40]:

mat=confusionMat(parsedDataT)
mat


# In[40]:




# # Graphlab-spark interface

# In[9]:

proj={"size.response":1,"request.pathID":1,"contentLeakage":1}
print proj

df=read_mongo(logs,query={}, projection=proj)


#df.take(1)


# In[13]:

get_ipython().magic(u'pylab inline')
import matplotlib.pyplot as plt
import graphlab

sf=graphlab.SFrame.from_rdd(df)


# In[14]:

sf.show()


# In[ ]:



