
# coding: utf-8

## Using GraphLab Create with Apache Spark

# In this notebook we demonstrate how to use Apache Spark with GraphLab Create. For this notebook, we will utilize [Apache Spark](http://spark.apache.org/) as a platform for doing large-scale data engineering.
# 
# The project is to learn a topic model using Wikipedia data, to see what topics are most represented in Wikipedia. The parts required for this project are:
# 1. [Set up environment](#Step-1:-Set-up-environment)
# 1. [Turn Raw Wikipedia text into Bag of Words, Using Spark](#Step-2:-Turn-Raw-Wikipedia-text-into-Bag-of-Words,-Using-Spark)
# 1. [Ingest Spark RDD as SFrame](#Step-3:-Ingest-Spark-RDD-as-SFrame)
# 1. [Learn Topic Model](#Step-4:-Learn-Topic-Model)
# 1. [Explore topics](#Step-5:-Explore-the-Topics)
# 1. [Save Results to Spark RDD](#Step-6:-Save-Results-to-Spark-RDD)
# 
# **Note:** Setting up Spark and PySpark are out of scope for this notebook, but are required for following along. 
# 
# By using PySpark and GraphLab Create together this notebook shows how easy it is to use both systems together.
# 
# #### Note: This notebook requires GraphLab Create 1.2.1 and Spark 1.1

#### Step 1: Set up environment

# There are many different ways to configure PySpark, but in order to use it in a standalone Python script (not in pysspark shell or using spark-submit) a handful of environment variables need to be set up correctly. The most convenient way to set these environment variables is by setting them in the shell configuration (ex. ```~/.bash_profile``` or ```~/.zshrc```). For instructive purposes, here are the variables that need to be set. 
# 
# **Note:** Running this notebook as is may not configure these environment variables correctly.

# In[37]:

# In order to be able to correctly import pyspark, configure SPARK_HOME and PYTHONPATH correctly
# These are one way to 
'''
!export HADOOP_CONF_DIR=$HOME/Venor/hadoop-1.2.1/
!export SPARK_HOME=$HOME/work/spark-1.2.0     # -bin-hadoop2.4
!export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
import os
os.environ['HADOOP_CONF_DIR'] = '%s/hadoop-2.x/etc/hadoop' % os.environ['HOME']
os.environ['SPARK_HOME'] = '%s/spark-1.1.1-bin-hadoop2.4' % os.environ['HOME']
os.environ['PYTHONPATH'] = '%s/python:%s' % (os.environ['SPARK_HOME'], os.environ.get('PYTHONPATH', ''))
'''


# GraphLab Create ships with a Spark Integration JAR, which is required in order to use PySpark with GraphLab Create. This JAR needs to be added to the Spark CLASSPATH. The following shell script will add the JAR to the ```spark-defaults.conf``` file. If running locally, you may want to configure the ```spark.driver.memory``` parameter to a larger value so the JVM doesn't run out of memory.

# In[41]:

get_ipython().run_cell_magic(u'bash', u'', u'export HADOOP_CONF_DIR=$HOME/hadoop-2.x/etc/hadoop\nexport SPARK_HOME=$HOME/spark-1.1.1-bin-hadoop2.4\nexport PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH\n\nif [ ! -f $SPARK_HOME/conf/spark-defaults.conf ]\nthen\n    echo "Copying spark-defaults.conf.template to spark-defaults.conf"\n    echo "If running Spark with \'local\' context, you may want to increase the spark.driver.memory parameter"\n    echo ""\n    cp $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf\nfi\n\nalready_exists=$(grep -c graphlab-create-spark-integration.jar $SPARK_HOME/conf/spark-defaults.conf)\nif [ $already_exists -eq 0 ]\nthen\n    echo "spark.driver.extraClassPath `python -c \'import graphlab as gl; print gl.get_spark_integration_jar_path();\'` " >> $SPARK_HOME/conf/spark-defaults.conf\n    echo "Added GraphLab Spark Integration JAR to $SPARK_HOME/conf/spark-defaults.conf"\nelse\n    echo "GraphLab Spark Integration JAR already added to Spark Configuration, doing nothing."\nfi\n\'\'\'')


#### Step 2: Turn Raw Wikipedia text into Bag of Words, Using Spark

# In[54]:

import graphlab as gl
from pyspark import SparkContext
import os
import requests


# In[55]:

# Set up the SparkContext object
# this can be 'local' or 'yarn-client' in PySpark
# Remember if using yarn-client then all the paths should be accessible
# by all nodes in the cluster.

#sc = SparkContext('local')


# Now that we have the SparkContext setup, let's download the Wikipedia data as an RDD. For this notebook we will only use a subset of the data, but there is code below to use the full dataset (which is about ~5GB).

# #### Download the Wikipedia Data

# In[56]:

import requests

def download_file(url, save_path):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(os.path.join(save_path, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

# File to download
file_list = [16] 

# If you want to use this entire Wikipedia dataset, uncomment the following line.
# This will download ~5GB of data split over 36 files.
# file_list = range(37)

# Download location for Wikipedia data
save_path = '/tmp/wikipedia'

# Actually download the files, if the location doesn't exist yet.
if not os.path.exists(save_path):
    os.mkdir(save_path)
    for idx in file_list: 
        url = 'http://s3.amazonaws.com/dato-datasets/wikipedia/raw/w%d' % idx
        print "Downloading '%s', saving to: '%s'" % (url, save_path)
        download_file(url, save_path) # This will download 146MB of data.


# In[57]:

rawRdd = sc.textFile('file:///%s/' % save_path).zipWithIndex()


# Now that the rdd is defined, let's see the first few lines to confirm it is structured the way we want.

# In[58]:

rawRdd.take(1)


# This looks good, it has a document on each line, with a subsequent index value. Since we want to split documents by space, it is important to remove any extra spaces that exist. When examining the document closely we see there are extra spaces, so let's clean those up and split each document by space. Also, let's put the index for the document as the first entry, so we have an 'id' key and then the words.

# In[59]:

# replace multiple spaces with a single space using re.sub, then trim whitespace and split on single space.
import re
splitRdd = rawRdd.map(lambda (a,b): (b, re.sub("[ ]+", " ", a).strip().split(" ")))
splitRdd.take(1)


# Now each document is a tuple of (index, list of words). Let's transform that into a list of (index, word) tuples instead. We will use flatMap for that.

# In[60]:

zipRdd = splitRdd.flatMap(lambda (a,b): zip([a] * len(b),b))
zipRdd.take(1)


# In[61]:

#zipRdd.map(lambda a: (a,1)).take(10)
rawRdd.count()


# Great, now we have things formatted the way we want, let's start aggregating to generate word counts per document.

# In[62]:

wordRdd = zipRdd.map(lambda composite_word: (composite_word, 1)).reduceByKey(lambda a, b: a + b)
wordRdd.take(10)


# And finally, let's create a dictionary with word as the key and count as the value.

# In[63]:

bagRdd = wordRdd.map(lambda (a,b):(a[0],(a[1],b))).groupByKey().map(lambda (a,b):(a,{word_count[0]:word_count[1] for word_count in b.data}))


# In[130]:

print bagRdd.count()
bagRdd.take(1) #[0][1]["2001"]


# In[ ]:

data=


#### Step 3: Ingest Spark RDD as SFrame

# Now that we have the raw Wikipedia text converted into a bag-of-words using Spark, it is easy to ingest that into GraphLab Create as an SFrame.

# In[133]:

data = gl.SFrame.from_rdd(bagRdd)


# In[135]:

data.column_names()


# In[137]:

gl.__VERSION__


# In[139]:

data[0]


# In[ ]:

#data = gl.SFrame.from_rdd(bagRdd)
data=data.unpack("X1").rename({"X1.0":"id", "X1.1":"bag_of_words"})
'''
data1=zip(*data["X1"])
data = gl.SFrame({'id':list(data1[0]), 'bag_of_words':list(data1[1])})
'''


# In[ ]:

data


# In[ ]:




# In[109]:




# In[110]:

gl.canvas.set_target('ipynb')
data.show()


# Looking at the most frequent words in the bag of words, it is obvious that 'stop words' are most prevalent. Let's remove them with one line, using GraphLab Create.

# In[115]:

gl.text_analytics.stopwords()


# In[113]:

# Trim out stopwords
data['bag_of_words'] = data['bag_of_words'].dict_trim_by_keys(gl.text_analytics.stopwords(), exclude=True)
data.show()


# In[119]:

len(data['bag_of_words'])


# Great, now the most frequent words are no longer stop words. We are ready to train a Topic Model on the data.

#### Step 4: Learn Topic Model

# Once we have an SFrame, training a Topic Model is one line. We are saying we are looking for the model to learn five topics, and to train for ten iterations.

# In[116]:

# If running on entire dataset, might want to increase num_topics and num_iterations
model = gl.topic_model.create(data['bag_of_words'], num_topics=5, num_iterations=10)


#### Step 5: Explore the Topics

# In[116]:




# First, let's get topic ids predicted from the model.

# In[117]:

pred = model.predict(data['bag_of_words'])
pred


# Well, that is just showing predicted topic_id. Instead, let's add a column with the topic_id we just predicted, and create that as our results SFrame.

# In[121]:

results = gl.SFrame({'doc_id':data['id'], 'topic_id':pred, 'bag_of_words':data['bag_of_words']})
results.swap_columns('doc_id', 'bag_of_words') # better SFrame formatting
results.print_rows(max_column_width=60)


# Now let's see which topic ids appear most frequently in this set of Wikipedia data

# In[122]:

gl.canvas.set_target('ipynb')
results['topic_id'].show('Categorical')


# Looking at this tells us that topic ids 3 and 2 are more common in this dataset. Let's find out what words are associated with those topics.

# In[123]:

model.get_topics([3], output_type='topic_words').print_rows(max_column_width=100)


# In[124]:

model.get_topics([2], output_type='topic_words').print_rows(max_column_width=100)


# Interesting. Wonder what this set of documents is about. Let's get the full list of topic words learned by the model.

# In[125]:

topics = model.get_topics()
topics = topics.rename({'topic':'topic_id'})
topics


# That SFrame is less useful, let's groupby all the same topic ids and create a list of words.

# In[126]:

topics.groupby(['topic_id'], {'topic_words':gl.aggregate.CONCAT("word")}).print_rows(max_column_width=80)


# This is the appropriate format for recording the topics learned, by topic_id.
# 
# Great, so now we have the results SFrame and the Topics SFrame, both of which can be saved back as Spark RDDs.

#### Step 6: Save Results to Spark RDD

# So now we have all the results ready as two SFrames. The first has the bag-of-words with the predicted topic_id, and the second has the topic words for each topic_id. These are both tables we can save as Spark RDDs, so subsequent Spark programs can utilize the findings from the Topic Model.

# In[127]:

# to save the predictions as an RDD
predictions_rdd = data.to_rdd(sc)
predictions_rdd.saveAsTextFile('file:///tmp/predictions.rdd')


# In[128]:

# save the topic_ids with their topic words
topics_rdd = topics.to_rdd(sc)
topics_rdd.saveAsTextFile('file:///tmp/topics.rdd')


# And that's it! GraphLab Create works well with Apache Spark, allowing you to leverage what you've already built in Spark with GraphLab Create. No need to save to intermediary formats just to train ML models in GraphLab Create.
# 
# For more information on using Apache Spark with GraphLab Create, check out the [User Guide section](http://dato.com/learn/userguide/#Spark_Integration).

# In[ ]:



