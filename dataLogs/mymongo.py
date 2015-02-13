import pymongo

#
# Connect to MongoDB server
#
def get_db(host="localhost", port=27017, username=None, password=None, db="dataLogs"):
    """ A util for making a connection to mongo """
    from pymongo import MongoClient
    #
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
#
    return conn[db]

def get_coll(host="localhost", port=27017, username=None, password=None, db="dataLogs",collection="logs"):
    db=get_db(host, port, username, password, db)
    return db[collection]

if __name__ == "__main__":
#if __name__=="__main__":
    logs = get_coll('localhost', 27017, None, None,"dataLogs", "logs")
    print logs.count()
