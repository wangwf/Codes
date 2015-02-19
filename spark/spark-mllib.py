
# coding: utf-8

# #Linear regression

# In[1]:

dataDir ="/home/wenfeng/work/spark-1.2.0/"


# In[2]:

from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from numpy import array

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.replace(',', ' ').split(' ')]
    return LabeledPoint(values[0], values[1:])

data = sc.textFile(dataDir+"data/mllib/ridge-data/lpsa.data")
parsedData = data.map(parsePoint)

# Build the model
model = LinearRegressionWithSGD.train(parsedData)

# Evaluate the model on training data
valuesAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))


# In[3]:

parsedData.take(2)


# #Linear Regression

# In[ ]:

from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.regression import LabeledPoint
from numpy import array

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.split(' ')]
    return LabeledPoint(values[0], values[1:])


data = sc.textFile(dataDir+"data/mllib/sample_svm_data.txt")
parsedData = data.map(parsePoint)

#parsedData.take(2)

# Build the model
model = LogisticRegressionWithSGD.train(parsedData)

# Evaluating the model on training data
labelsAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())
print("Training Error = " + str(trainErr))


# In[ ]:

for d in parsedData.take(2): #.collect():
    print d


# In[ ]:

parsedData.take(2)


# #Decision Tree -- Classification

# In[3]:

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.util import MLUtils

# Load and parse the data file into an RDD of LabeledPoint.
data = MLUtils.loadLibSVMFile(sc, dataDir+'data/mllib/sample_libsvm_data.txt')
# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a DecisionTree model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
model = DecisionTree.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},
                                     impurity='gini', maxDepth=5, maxBins=32)

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
print('Test Error = ' + str(testErr))
print('Learned classification tree model:')
print(model.toDebugString())


# #Decision Tree -- Regression

# In[4]:

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.util import MLUtils

# Load and parse the data file into an RDD of LabeledPoint.
data = MLUtils.loadLibSVMFile(sc, dataDir+'data/mllib/sample_libsvm_data.txt')
# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a DecisionTree model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
model = DecisionTree.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                    impurity='variance', maxDepth=5, maxBins=32)

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression tree model:')
print(model.toDebugString())


# In[31]:

for d in data.take(10): #take(10):
    print d.features.squared_distance


# In[25]:

for d in data.take(1):
    print d.features.values


# #Clustering -- Kmean

# In[2]:

from pyspark.mllib.clustering import KMeans
from numpy import array
from math import sqrt

# Load and parse the data
data = sc.textFile(dataDir+"data/mllib/kmeans_data.txt")
parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))

# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 2, maxIterations=10,
        runs=10, initializationMode="random")

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))


# In[3]:

type(parsedData)


# In[4]:

parsedData.take(1)


# In[4]:




# #Naive Bayes

# In[37]:

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes


# Load and parse the data
def parsePoint(line):
    value0,value1 = line.split(',',1)
    value1 = [ float(x) for x in value1.split(" ")]
    return LabeledPoint(value0, value1)


#data = sc.textFile(dataDir+"data/mllib/sample_svm_data.txt")
data = sc.textFile(dataDir+ "data/mllib/sample_naive_bayes_data.txt" )

parsedData = data.map(parsePoint)


# In[38]:

data.take(2), parsedData.take(2)


# In[39]:

# Train a naive Bayes model.
model = NaiveBayes.train(parsedData, 1.0)

# Make prediction.
prediction = model.predict(parsedData)


# In[49]:

data = sc.parallelize([
  LabeledPoint(0.0, [0.0, 0.0]),
  LabeledPoint(1.0, [2.0, 0.0]),
  LabeledPoint(0.0, [0.0, 0.0]),
  LabeledPoint(1.0, [0.0, 2.0]),
  LabeledPoint(0.0, [0.0, 0.0]),
  LabeledPoint(1.0, [3.0, 3.0])
])

# Train a naive Bayes model.
model = NaiveBayes.train(data, 1.0)

# Make prediction.
prediction = model.predict(data)


# In[48]:

prediction.count()


# In[ ]:



