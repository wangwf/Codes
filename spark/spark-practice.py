
# coding: utf-8

# #SPark
# To launch PySpark in Ipython, set the IPYTHON variable to 1 when running bin/pyspark
#  $IPYTHON=1 ./bin/pyspark
# 
#  Alternatively, you can customize. to launch the IPython Notebook with Pylab
# 
#  $IPYTHON_OPTS="notebook --pylab inline" ./bin/pyspark

# #Functional
# * map
# * reduce
# * filter
# * lambda
# * itertools, pytoolz
# 

# In[1]:

lambda_square = lambda x: x*x
map(lambda_square, range(10))


# In[2]:

# reduce apply a function with two arguments cumulatively to the container
reduce(lambda x,y: x+y, range(10))


# In[3]:

#filter, constructs a new list for items where the applied function is true
filter(lambda x: x%2==0, range(10))


# In[4]:

'''
from pyspark import SparkContext
if 'sc' not in globals():
    CLUSTER_URL= # "spark://ec2-50-16-173-245.compute-1.amazonaws.com:7077"
    sc = SparkContext(CLUSTER_URL,"example")
else:
    print "sc is here"
    '''


# #Spark 
# 
# Actions return values
# 
# * collect,    Returns a list from all elements of an RDD
# * reduce
# * take
# * count
# 
# Transformations returns pointers to new RDDs
# 
# * map, flatmap
# * reduceByKey
# * filter
# * glom,     returns an RDD list form each partition of an RDD
# 

# In[5]:

import numpy as np

rdd = sc.parallelize(np.arange(20), numSlices =5)


# In[6]:

rdd.count()


# In[7]:

for x in rdd.glom().collect():
    print x


# In[8]:

rdd = sc.parallelize(np.arange(20), numSlices=10)
for x in rdd.glom().collect():
    print x


# # map and Flatmap

# In[9]:

rdd = sc.parallelize([ [2, 3, 4],[0, 1],[5, 6, 7, 8] ])
rdd.collect()


# In[10]:

rdd.map(lambda x: range(len(x))).collect()


# In[11]:

rdd.flatMap(lambda x: range(len(x))).collect()


# # reduce
# * reduce()
# * reduceByKey()
# * countByKey()
# 

# In[12]:

#reduce
rdd.flatMap(lambda x:x).reduce(lambda x,y: x+y)


# In[13]:

rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 2)])
rdd.collect()


# In[14]:

rdd.reduceByKey(lambda x,y:x+y).collect()


# In[15]:

rdd.countByKey()


# #Computation

# In[16]:

import time
import os

def work(x):
    start_time = time.time()
    time.sleep(x)
    end_time = time.time()
    return {'id':os.getpid(), 'start':start_time, 'end_time':end_time}



# In[17]:

import numpy as np
np.random.seed(1045)
job_times = np.random.uniform(0.4, 0.6, 240)


# In[18]:

print 'Estimated serial time = {0:0.2f}'.format(job_times.sum())
print 'Amdahls parallel time = {0:0.2f}'.format(job_times.sum()/12.)


# In[19]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import pandas as pd

def plot_workflow(results):
    res = pd.DataFrame(results)
    ids = list(set(res['id']))
    id_dic = dict( [k,v+0.65] for k,v in zip(ids, range(len(ids))))
    fig, ax = plt.subplots(figsize=(8, 6))

    tmin = res['start'].min()    
    for i in res.index:
        x_start = res.ix[i]['start'] - tmin
        x_end = res.ix[i]['end_time'] - tmin - x_start
        x_id = id_dic[res.ix[i]['id']]
        ax.add_patch(plt.Rectangle((x_start, x_id), 
                                   x_end, 0.8, 
                                   alpha=0.5, 
                                   color='grey'))
    
    ax.set_ylim(0.5, len(ids)+0.5)
    ax.set_xlim(0, res['end_time'].max() - tmin)
    ax.set_ylabel("Worker")
    ax.set_xlabel("seconds")


# In[20]:

jobs = sc.parallelize(job_times)
print jobs.count()
results = jobs.map(work)
get_ipython().magic(u'time res = results.collect()')


# In[21]:

plot_workflow(res)


# In[22]:

import numpy as np
data = np.arange(1000).reshape(100,10)
print data.shape


# In[23]:

import pandas as pd

tmp = pd.DataFrame(data, 
             columns=['x{0}'.format(i) for i in range(data.shape[1])])
tmp.head()


# In[24]:

tmp.sum(axis=1)


# In[25]:

tmp.to_csv("numbers.csv",index=False)


# In[25]:




# In[26]:

lines = sc.textFile('numbers.csv')


# In[27]:

lines.take(2)


# In[28]:

for l in lines.take(2):
    print l


# In[29]:

lines.take(1)[0].find("x")


# In[30]:

lines = lines.filter(lambda x: x.find('x') !=0)
for l in lines.take(2):
    print l


# In[31]:

data = lines.map(lambda x: x.split(","))
data.take(3),data.count()


# In[32]:

# Row sum

def row_sum(x):
    int_x = map(lambda x: int(x), x)
    return sum(int_x)

data_row_sum = data.map(row_sum)


# In[33]:

print data_row_sum.collect()
print data_row_sum.count()


# In[34]:

# Col Sum
def col_key(x):
    for i,value in enumerate(x):
        yield (i, int(value))
        
tmp = data.flatMap(col_key)
tmp.take(3)


# In[35]:

tmp = tmp.groupByKey()
'''
for i in tmp.take(2):
    print type(i),i[1]
    for ii in i[1]:
        print ii
'''
'''
tmp = tmp.groupByByKey()
for i in tmp.take(2):
    print i
    '''


# In[36]:

data_col_sum = tmp.map(lambda x: sum(x[1]))
for i in data_col_sum.take(2):
    print i


# In[36]:




# In[37]:

points = sc.textFile('iris_train.csv',10) #across 10 cpus
points.take(5)


# In[38]:

from pyspark.mllib.classification import LogisticRegressionWithSGD

#parsed_data = points.map(lambda line: np.array([float(x) for x in line.split(',')[:4]]))
#parsed_data.take(5)
#points.map(lambda line: x for x in line.split(','))
points = points.filter(lambda x: x.find("sepal")!=0)    .map(lambda line: line[:line.rfind(",")])    .map(lambda line:  np.array([float(x) for x in line.split(',')[:4]])) 
points.take(2)


# In[39]:

parsed_data = points
model = LogisticRegressionWithSGD.train(parsed_data)

y = parsed_data.map(lambda x: int(x[0]))
y.take(5)


# In[ ]:







# In[ ]:




# In[ ]:




# In[ ]:

from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.regression import LabeledPoint
from numpy import array

# Load and parse the data
def parsePoint(line):
    values = [float(x) for x in line.split(' ')]
    return LabeledPoint(values[0], values[1:])

dataDir ="/home/wenfeng/work/spark-1.1.0/"
data = sc.textFile(dataDir+"data/mllib/sample_svm_data.txt")
parsedData = data.map(parsePoint)

parsedData.take(2)
'''
# Build the model
model = LogisticRegressionWithSGD.train(parsedData)

# Evaluating the model on training data
labelsAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())
print("Training Error = " + str(trainErr))
'''


# In[ ]:



