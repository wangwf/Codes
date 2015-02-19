
# coding: utf-8

# # Data Wrangle in MongoDB
# 
# <ul>
# <li> 1. Query data in MongoDB  </li>
# <li> 2. Extract data array for building model  </li>
# <li> 3. Visualize data using Matplotlib </li>
# <li> 4. Variable importance, correlation matrix or mutual information?</li>
# <li> 5. Extract into dataframe format? mongoDB pipe to Pandas/Graphlab?
# <li> 6. Time plot (response size, Normalized Compression Distance)</li>
# </ul>
# 
# Explore Mongo data, produced from extract.ipynb.
# 
# ## 1. Query data in MongoDB

# In[97]:

get_ipython().magic(u'pylab inline')
import matplotlib.pyplot as plt


# In[98]:

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
tests = get_coll('localhost', 27017, None, None,"dataLogs", "test")


# In[99]:

#
# peek one record
#
logs.find_one()


# In[100]:

#
# Extract all features in the first event
#
features=logs.find_one().keys()  # list of features
features.remove("_id")  # _id is useless for this study
import unicodedata
features = [x.encode("UTF8") for x in features] 
features


# In[101]:

# Simple query to peek Content-Type variable
#
query ={"response.headers.content-type":{'$exists':True}}
iter=logs.find(query,{"_id":0,"response.headers.content-type":1},limit=10)
from pprint import pprint
for item in iter:
    print pprint(item)


# In[102]:

#find distinct values in field 

featuresRequest=["httpversion", "address",#"client_conn", # "requestcount",
                 "error","port",
                    "scheme","path","host", "headers","content","method",
                    #"ssl_setup_timestatmp","timestamp_end","timestamp_start", "tcp_setup_timestamp"
                    "ip","msg"] #,"cookie"]
    
featuresHeaders=["X-Frame-Options","X-Xss-Protection","X-Content-Type-Options","X-Ua-Compatible",
               "X-Xhr-Current-Location","Content-Type","Etag","Cache-Control",
               "X-Request-Id","X-Runtime",
               "Server","Date",
               "Content-Length", "connection","Set-Cookie"]

featuresRequest=["request."+f for f in featuresRequest]
for q in featuresRequest:
    print "%s has the below distinct values:"%q
    print logs.distinct(q)
    print "\n"



# # response vs path

# In[102]:




# In[103]:

pathOptions = logs.distinct("request.path")
pathOptions = [x.encode('UTF8') for x in pathOptions]
y_pos       = range(len(pathOptions))

minMaxR=logs.aggregate([{"$group":
                          {"_id":"$"+"request.path",
                           "minRes":{"$min":"$size.response"},
                           "maxRes":{"$max":"$size.response"},
                           "avgRes":{"$avg":"$size.response"}
                           }},
                        {"$sort":{"_id":1}}   #{"avgRes":-1}}
                        ])



minMaxRt=tests.aggregate([{"$group":
                          {"_id":"$"+"request.path",
                           "minRes":{"$min":"$size.response"},
                           "maxRes":{"$max":"$size.response"},
                           "avgRes":{"$avg":"$size.response"}
                           }},
                        {"$sort":{"_id":1}}   #{"avgRes":-1}}
                          ])
#minMaxR["result"]
#len([m['_id'] for m in minMaxRt["result"]])


# In[103]:




# In[104]:

options1 = [m['_id'] for m in minMaxR["result"]]
options2 = [m['_id'] for m in minMaxRt["result"]]

options = list(set().union(options1 +options2))
len(options)
for item in options:
    if item not in options1:
        minMaxR['result'].append({"_id":item, "avgRes":0,"minRes":0,"maxRes":0})
    if item not in options2:
        minMaxRt['result'].append({"_id":item, "avgRes":0,"minRes":0,"maxRes":0})
 
#list(set(options1) | set(options2))
[x for x in options1 if x not in options2]


# In[104]:




# In[105]:


minMaxR["result"]  = sorted(minMaxR["result"],  key=lambda x: x["_id"])
minMaxRt["result"] = sorted(minMaxRt["result"], key=lambda x: x["_id"])

  
#for key in ['/users/3', '/users/3/followers']:
#print [ x for x in minMaxRt["result"] if x["_id"] in ['/users/3', '/users/3/followers','/contact','/users/1/edit']]
#print len(avgRes),len(avgResT)


# In[105]:




# In[106]:

#for i in range(len(avgRes)):    print int(avgRes[i]),int(avgResT[i])
import numpy as np
avgRes  = np.array([m['avgRes'] for m in minMaxR["result"]])
avgResT = np.array([m['avgRes'] for m in minMaxRt["result"]])
options = np.array([m['_id'] for m in minMaxR["result"]])


# In[107]:

# standard deviation
res=[]
for o in options:
    iter=logs.find({"request.path":o},{ "size.response":1})
    res.append([x["size"].get("response") for x in iter])
res = np.array(res)
avgResStd = [np.std(x) for x in res]

#for i in range(len(options)):    print options[i], res[i],avgRes[i], np.mean(res[i]), np.std(res[i])


# In[107]:




# In[108]:

get_ipython().magic(u'pylab inline')
import matplotlib.pyplot as plt

rcParams['figure.figsize'] = 15, 20

fig = plt.figure()
ax = fig.add_subplot(111)

#plt.barh([y+0.1 for y in y_pos], avgRes[::-1], height=0.4, align='center', alpha=0.4,color="b", linewidth=0.01,xerr=avgResStd)
plt.barh([y+0.1 for y in y_pos], avgRes[::-1], height=0.4, align='center', alpha=0.4,color="b", linewidth=0.01)
#plt.errorbar(avgRes, [y+0.1 for y in y_pos], xerr=avgResStd,yerr=None, fmt='')
plt.barh([y-0.1 for y in y_pos], avgResT[::-1],height=0.4, align='center', alpha=0.5,color="r")

plt.xlim(0,)
plt.yticks(y_pos, options[::-1])
plt.xlabel("Average Response Size")
plt.title("Average Response Size vs path, learnData (Blue) -- malformed (red)")


# In[108]:




# In[108]:




# In[108]:




# In[109]:

def plotFeatureDepence(dbColl,feature, ncols=4, figureSize=(15,20)):
    
    Options = dbColl.distinct(feature)
    Options = [x.encode('UTF8') for x in Options]
    #print Options
    res =[]
    for p in Options:
        query={feature:p}
        iter = dbColl.find(query)
        res.append([item["size"].get("response") for item in iter])

       #for i in len(pathOptions):
    from math import ceil 
#    ncols =4
    nrows = int(math.ceil(len(res)*1.0/ncols))

    rcParams['figure.figsize'] = figureSize #15, 20
    fig, axes = plt.subplots(nrows, ncols)
    fig.tight_layout()
    for i in range(len(res)):
        ax = plt.subplot(nrows,ncols, len(res)-i-1)
        #   plt.subplots_adjust(hspace = .001)
        minX =0
        maxX = int(1.1*max(res[i]))
        #print maxX, res[i]
        ax.set_xlim(minX, maxX)
        ax.hist(res[i], bins=20,range=(minX,maxX))
        plt.title(Options[i])


# In[110]:

F="request.path"
print "learnDataSet.log", F
plotFeatureDepence(logs, F,ncols=4, figureSize=(15,20))


# In[111]:

F="request.path"
print "malformed.log", F
plotFeatureDepence(tests, F,ncols=4, figureSize=(15,20))


# In[112]:

F="request.method"
print "learnDataSet.log", F
plotFeatureDepence(logs,F,ncols=2, figureSize=(10,5))


# In[113]:

F="request.method"
print "malformed", F
plotFeatureDepence(tests,F,ncols=2, figureSize=(10,5))


# In[114]:


F="response.headers.content-type"
print F
plotFeatureDepence(logs, F,ncols=2, figureSize=(10,5))


# In[115]:

print " malformed.log ", F
plotFeatureDepence(tests, F,ncols=2, figureSize=(10,5))


# In[116]:

F="response.headers.content-type"
print F
plotFeatureDepence(logs, F,ncols=2, figureSize=(10,5))


# In[116]:




# #2 Check Content-Length, content, headers and response values
# 
# There are several features related to the request size: Content-Length, content, headers and response.
# 

# In[117]:

#
#  feature-dependence using mongodb's group operation
#    (min, max, average)
#
def variableDependenc(field):
    minMaxR=logs.aggregate([{"$group":
                          {"_id":"$"+field,
                           "minRes":{"$min":"$size.response"},
                           "maxRes":{"$max":"$size.response"},
                           "avgRes":{"$avg":"$size.response"}
                           }}]
                         )
    print "\n=== %s min max avg======"%field
    for item in minMaxR['result']:
        print item["_id"],item["minRes"],item["maxRes"], item["avgRes"]
    return minMaxR
        
    
for f in ["method","path"]:
    variableDependenc(f)


# In[118]:

logs.aggregate([{"$project":
                 {
                 "response.headers.content-length":"$response.headers.content-length",
                 "size.content":"$size.content",
                 "diff": {"$subtract":["$response.headers.content-length","$size.content"]}
                 }}
                ])

'''
for item in iter:
    print item
logs.find_one({},{"response.headers.content-length":1, "size.content":1})
'''


# In[119]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt 
import mpld3
mpld3.enable_notebook()



# In[120]:

iter=logs.find({"size.headers":{'$exists':True}},{"_id":0, "size.headers":1})
hsize =[int(item['size'].values()[0]) for item in iter]

#plt.interactive(True)
plt.title("headers-size hist")
plt.xlabel("headers")
plt.hist(hsize,bins=100)
plt.show()
#mpld3.show


# In[121]:


responseSize ="response"
iter=logs.find({"or":[{"size.response":{'$exists':False}}, {"size.response":0}]})
t= [item['size'] for item in iter]
print "%s \'response\' doenot exist or zero-value! \n "%len(t)


query ={"size.response":{'$exists':True}}

iter=logs.find(query,{"_id":0, "size.response":1})
rsize =[int(item['size'].values()[0]) for item in iter]


#plt.interactive(True)
plt.title("response size hist")
plt.xlabel("response")
plt.hist(rsize,bins=50, normed=1, histtype="stepfilled", log=True)


# # 3. Feature dependence study
# 
# * "X-Runtime", "timestamp_end","timestamp_start",
# * "X-Frame-Options","X-Xss-Protection","X-Content-Type-Options","X-Ua-Compatible","X-Xhr-Current-Location"
# * "Content-Type","Etag","Cache-Control", "Server","Date",
# * "cert","code","requestcount",
# * "port","scheme","http","path","host","headers", "Connection",
# * "ip","Referer"
# * "Accept-Encoding","Accept-Language","method","msg"

# In[122]:

f="x-runtime"

def featureDependence(f):
    iter = logs.find({"size.response":{"$exists":True},"response.headers."+f:{"$exists":True}},
                     {"_id":0, "size.response":1,  "response.headers."+f:1})
    
   # f =str([[x] for x in f.split(".")]).replace(", ","")[1:-1]
    
    x,y=[],[]
    for item in iter:
        y.append(int(item['size']["response"]))
        x.append(float(item["response"]["headers"][f]))
        
    print len(x),len(y)
    title="Response vs %s"%f
    plt.figure(title)
    plt.title(title)

    plt.xlabel("Variable-%s"%f,fontsize="x-large")
 
    plt.plot(x,y,"bs") 


    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    # 




# In[123]:

# X-Runtime

featureDependence(f="x-runtime")    


# In[124]:

#requestCount
featureDependence(f="requestcount")    


# In[125]:

f="method"
def checkFeatureDependence(f, option=0):
    Rm = variableDependenc(f)
    ymin = [int(item.get("minRes") or 0) for item in Rm["result"]]
    ymax = [int(item.get("maxRes") or 0) for item in Rm["result"]]
    yavg = [int(item.get("avgRes") or 0) for item in Rm["result"]]

    xTicks=[str(item.get("_id")) for item in Rm["result"]]
    #    print item.get("minRes")  #.get("minRes")
    xTicks
    import numpy as np
    x= np.arange(len(xTicks))

    title="Response vs %s"%f
    plt.figure(title)
    plt.title(title)
    #ax = fig.add_subplot(111)
    #xtickNames = ax.set_xticklabels(xTicks)
    #plt.setp(xtickNames, rotation=45, fontsize=100)

    plt.xlabel("Variable-%s"%f,fontsize="x-large")
    #plt.ylabel("size")

    if option==0:
        plt.plot(x-0.1, ymin,"bo", x+0.1, ymax,"rs", x,yavg,"g^")
    elif option ==1:
        plt.plot(x,ymax,"g^")  # only show average

    plt.xticks(x, xTicks, rotation='vertical')

    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    #plt.show()
    print x,xTicks
    


# In[126]:

# method  = "GET" or "post"
checkFeatureDependence(f="method")


# In[127]:

# path
checkFeatureDependence(f="path", option=0)


# In[128]:

# path
checkFeatureDependence(f="Content-Type", option=0)


# In[129]:

# code = 200, 302, 304
checkFeatureDependence(f="code", option=0)


# In[129]:




# # 4. Data Reshape to Pandas dataframe
# 

# In[130]:

import pandas as pd


#def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
def read_mongo(collection, query={},host='localhost',no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Make a query to the specific DB and Collection
    cursor = collection.find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

df=read_mongo(logs,{})
df_test = read_mongo(tests)


# In[131]:

df[:5]


# In[132]:

len(df)


# In[133]:

df['response'][0]["headers"]


# In[134]:

#df.dropna()
#df["timeStampStartEnd"]=df['timestamp_end'].astype(float) - df['timestamp_start'].astype(float)
#df_test["timeStampStartEnd"]=df_test['timestamp_end'].astype(float) - df_test['timestamp_start'].astype(float)
df.columns, df.index


# In[135]:

# Writing Pandas dataframe to CSV file
#df.to_csv("output3_df.txt",sep=",")
#df_test.to_csv("test_df.txt",sep=",")


# In[136]:

#df.ix[:,["response"]].ix[3:5,].columns


#df1
pd.DataFrame(df.ix[:10,['request',"size","contentLeakage"]])


# In[137]:

# Correlation matrix between
# 
#
#df.ix[:,['Content-Length','content','response', "headers","X-Runtime"]].astype(float).corr()

#df1 = pd.DataFrame( [x['path'] for x in df.ix[:,"request"]])
#df = pd.DataFrame(,columns=["response","content","headers"])


df1=[]
for x in df['size'][:]:
    df1.append( [x["response"], x["content"],x["headers"] ])

dfx=pd.DataFrame(df1, columns=["response","content","headers"])
dfx.astype(float).corr()


# In[138]:

#rcParams['figure.figsize'] = 5,5
plt.figure(figsize=(5,5))
plt.clf()
#df["contentLeakage"].hist()


# In[139]:

def getDF(df):
    df1=[]
    for i in range(len(df)):
        alist=[df['size'][i]['response'], df['request'][i]['path'], df['response'][i]['headers'].get("x-runtime") or 0]
        alist.append(df["contentLeakage"][i])
        df1.append(alist)
    return pd.DataFrame(df1,columns=["response","path","x-runtime","contentLeakage"])
        
df1=getDF(df)

'''
df1=[]
#df["request"][0]["path"],df["size"][0]["response"],len(df)
    #df1.append( [x["response"], x["content"],x["headers"] ])
for i in range(len(df)):
    df1.append( [df['size'][i]['response'], df['request'][i]['path'], df['response'][i]['headers'].get("x-runtime") or 0])
'''
df1.to_csv("test.csv")
df1[:5]


# In[140]:

dft=getDF(df_test)
dft[:5]


# In[141]:

df1=pd.read_csv("test.csv")
type(df1[["response","path"]])


# In[142]:

paths = pd.Series(df1[['path']].values.ravel()).unique()
paths


# In[143]:

df1["pathID"] = [np.where(paths==p)[0][0] for p in df1["path"]]
#plt.plot(df1['response'],pathID,kind )
#df2=df1[["response","pathID"]]
dft["pathID"] = [np.where(paths==p)[0][0] for p in dft["path"]]


# In[143]:




# In[145]:

#plt.scatter(df1['response'],df1['pathID'],c=df1['pathID'])

def plotPath(df1, dft, xmax):
    plt.clf()
    rcParams['figure.figsize'] = 15, 25
    fig=plt.figure()
    ax = fig.add_subplot(111)

    from math import log
    #res = [log10(x+1) for x in df1['response']]
    
    X = [log10(x+1) for x in df1['response']] 
    Y = [ y+0.05 for y in df1['pathID']]
    C = [ c for c in df1['contentLeakage']]

    
    Xt = [log10(x+1) for x in dft['response']] 
    Yt = [ y-0.05 for y in dft['pathID']]
    Ct = [c for c in dft['contentLeakage']]

    
#    ax.set_yticklabels(paths)

    l1=ax.scatter( X, Y, c=C, marker="o", facecolors="none") #c=dft['pathID'])
    l2=ax.scatter( Xt, Yt, c=Ct,marker="s", facecolors="none") #c=dft['pathID'])

    plt.legend((l1,l2),("LearnData","Malformed (blue-normal, red-leakage )"), scatterpoints=1)
    plt.yticks(range(len(paths)), list(paths))
 
#    plt.yticks(range(len(paths)), list(paths))
    yt = [item.get_text() for item in ax.get_yticklabels()]
#    print yt,len(yt)
 
    plt.xlim(0,xmax)
    plt.ylim(-1,len(paths)+1)

    plt.xlabel("Response size-log10()")
    plt.title("Response Size (log10) vs path")
#    plt.savefig("responseVspath.png")

xmax = log(df1['response'].max())
plotPath(df1,dft,xmax)


# # Map/Reduce

# In[146]:

from bson.code import Code

map    = Code("function(){"
              "   emit(this.request.path, 1);"
              "}")
            

reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i];"
               "  }"
               "  return total;"
               "}")


results =logs.map_reduce(map, reduce, "myresult") #, full_response=True)
for doc in results.find():
    print  int(doc["value"]), doc["_id"]

#logs.find_one()


# In[147]:

#
#  Standard deviation for each path-option
#
map    = Code("function(){"
              "   emit(this.request.path, this.size.response);"
              "}")
            
'''
reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i];"
               "  }"
               "  return total;"
               "}")
'''
reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i];"
               "  }"
               "  var avg= total/values.length;"
               "  var sqr=0;"
               "  for (var i = 0; i < values.length; i++){"
               "    var diff = values[i] - avg ;"
               "    sqr += diff*diff;"
               "  }"
               "  return sqr;"
               "}")

import math
results =logs.map_reduce(map, reduce, "myresult") #, full_response=True)
for doc in results.find():
    print  int(math.sqrt(doc["value"])), doc["_id"]


# In[148]:

# pr

from pymongo import MongoClient
from bson.code import Code

mapper = Code("""
    function() {
                  for (var key in this.request) { emit(key, null); }
               }
""")
reducer = Code("""
    function(key, stuff) { return null; }
""")

distinctThingFields = logs.map_reduce(mapper, reducer
    , out = {'inline' : 1}
    , full_response = True)
## do something with distinctThingFields['results']
for item in distinctThingFields["results"]:
    print item["_id"]


# In[148]:




# In[148]:




# In[148]:




# # time Series plot

# In[149]:

get_ipython().magic(u'pylab inline')
import matplotlib.dates as md
import matplotlib.pyplot as plt

import math
import numpy as np
import datetime as dt
import time

#responseSize 
iter=logs.find({},{"_id":0, "size.response":1, "request.timestamp_start":1, "response.headers.timestamp_end":1})

responseSize = []
timeStamps   = []

for item in iter:
    responseSize.append( math.log10(item["size"]["response"] +1) )
    timeStamps.append( item["response"]["headers"]["timestamp_end"] )
    #timeStamps.append( item["request"]["timestamp_start"] )

#sort two lists together
timeStamps,responseSize= zip(*sorted(zip(timeStamps,responseSize)))


# In[149]:




# In[150]:

dt1= [ dt.datetime.fromtimestamp(ts) for ts in timeStamps]
datenums=md.date2num(dt1)

plt.clf()

plt.subplots_adjust(bottom=0.2)
plt.xticks(rotation=25)
ax =plt.gca()
xfmt = md.DateFormatter("%H:%M:%S") #'%Y-%m-%d %H%M:%S')
ax.xaxis.set_major_formatter(xfmt)

plt.plot(datenums,responseSize)
plt.ylabel("Response size (log10)")
plt.xlabel("request start time")
#plt.show()


# In[151]:

#ds,de = dt.datetime.fromtimestamp(min(timeStamps)), dt.datetime.fromtimestamp(max(timeStamps))

dt1[0],dt1[-1]


# In[152]:

plt.plot(responseSize)


# # NCD or other similarity function

# In[153]:

#ts = pd.Series(responseSize, index=pd.date_range(start=dt1[0], periods=len(responseSize), freq="0.00001s"))
#ts = ts.cumsum()  # return cumulative sum ax =plt.gca()
#ts.plot()

import gzip
def gzipCompression(text):
    return len(gzip.zlib.compress(text))
'''
import lzma
def  lzmaCompression(text):
    return len(lzma.compress(text))
'''
def ncd(w1, w2):
    l1  = gzipCompression(w1)
    l2  = gzipCompression(w2)
    l12 = gzipCompression(w1+w2)
    #print l1,l2,l12
    return 1.0*(l12 - min(l1,l2))/max(l1,l2)

iter=logs.find() #{},{"_id":0, "size.response":1, "request.timestamp_start":1, "response.headers.timestamp_end":1})
refDoc="{'response':{'header':{},'content':''}}"
compressSize = [ ncd(str(item),refDoc ) for item in iter]


plt.figure()
plt.clf()
#plt.plot(compressSize)
plt.subplots_adjust(bottom=0.2)
plt.xticks(rotation=25)
ax =plt.gca()
xfmt = md.DateFormatter("%H:%M:%S") #'%Y-%m-%d %H%M:%S')
ax.xaxis.set_major_formatter(xfmt)

plt.plot(datenums,compressSize)
plt.ylabel("Compression distance ")
plt.xlabel("request start time")


# In[161]:



iter=logs.find({"request.path":paths[1]}) #{},{"_id":0, "size.response":1, "request.timestamp_start":1, "response.headers.timestamp_end":1})

compressSize=[]
refDoc=""
for item in iter:
    if refDoc=="":
        refDoc = str(item)
    else: 
#        print refDoc
        compressSize.append(ncd(str(item),refDoc ))


plt.figure()
plt.clf()

print paths[0],len(compressSize)
plt.hist(compressSize)
plt.ylabel("Compression distance ")
plt.xlabel("request start time")

