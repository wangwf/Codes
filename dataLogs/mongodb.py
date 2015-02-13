
# coding: utf-8

# # Data Wrangle in MongoDB
# 
# <ul>
# <li> 1. Query data in MongoDB  </li>
# <li> 2. Extract data array for building model  </li>
# <li> 3. Variable importance, correlation matrix or mutual information?</li>
# <li> 4. Extract into dataframe format? mongoDB pipe to Pandas/Graphlab?
# </ul>
# 
# ## 1. Query data in MongoDB

# In[7]:

import pymongo


def get_db(host, port, username, password, db):
    """ A util for making a connection to mongo """
    from pymongo import MongoClient
    
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

#connection = pymongo.Connection("mongodb://localhost", safe=True)
#db=connection.dataLogs
#logs=db.logs    #collections name

db = get_db('localhost', 27017, None, None,"dataLogs")
logs= db.logs


# In[8]:

logs.find_one()


# In[9]:

d=logs.find_one()
features=d.keys()
features


# In[10]:

query ={"Content-Type":{'$exists':True}}
iter=logs.find(query,{"_id":0,"Content-Type":1},limit=10)
for item in iter:
    print item


# In[11]:

#find distinct values in field content-Type

for q in ["Content-Type","X-Content-Type-Options", "X-Xhr-Current-Location","Cache-Control"]:
    print q,logs.distinct(q)


# In[13]:




# In[14]:

n=1
try:
    iter = logs.find({},limit=10, skip=n)  #.sort('Content-Length', direction=1)
    for item in iter:
        print "Content-Length",item['Content-Length']
except:
    print "Error trying to read collection:", sys.exc_info()[0]


# #2 Extract data array for building model

# In[15]:

query ={"Content-Length":{'$exists':True}}
iter=logs.find(query,{"_id":0,"Content-Length":1})
#for item in iter:
#    print item, type(item), int(item.values()[0])
rsize =[int(item.values()[0]) for item in iter]


# In[16]:

import matplotlib.pyplot as plt
plt.figure("response/runtime")
#plt.xlabel("runtime")
#plt.ylabel("size")
plt.plot(rsize)
plt.show()


# In[34]:

query ={"Content-Length":{'$exists':True}, "Content-Type':{'$exist':True}, }
iter=logs.find(query,{"_id":0,"Content-Length":1})
#for item in iter:
#    print item, type(item), int(item.values()[0])
#rsize =[int(item.values()[0]) for item in iter]
features


# # Data Reshape to Pandas dataframe

# In[17]:

import pandas as pd


#def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
def read_mongo(collection, query={}, host='localhost',no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    #    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = collection.find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

df=read_mongo(logs)


# In[18]:

df


# In[19]:

# Writing Pandas dataframe to CSV file
df.to_csv("output3_df.txt",sep=",")


# In[ ]:



