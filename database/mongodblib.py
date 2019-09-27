#
# base connection for TinyDB 
#
from redmonty.config import database
#from pymongo import MongoClient
import pymongo
import urllib

mongodb_conf= database.get("mongodb", None)
mongodb = None

if not mongodb_conf["atlas"]:
    # normal mongodb server (local or remote)
    conn_str = "mongodb://" + mongodb_conf["host"] + ":" + str(mongodb_conf["port"]) + "/"    
    print(" ... setting it up for mongoDB: " + conn_str)
    client = pymongo.MongoClient(mongodb_conf["host"], mongodb_conf["port"])
    #db = client[mongodb_conf["dbname"]]
    #collection=db[mongodb_conf["dbname"]]

else:
    # go cloudy &  set it up for atlas use
    if not mongodb_conf["urlencode"]:
        conn_str = mongodb_conf["atlas_cstr"]
        print(" ... setting it up for mongoDB Atlas: {}".format( conn_str[conn_str.index(r"@"):] ))
    else:
        conn_str="mongodb+srv://" + urllib.parse.quote(mongodb_conf["atlas_user"]) + ":" 
        conn_str += mongodb_conf["atlas_pwd"] + r"@" + mongodb_conf["atlas_cstr"]
        print(" ... setting it up for mongoDB Atlas: ({}) @{} ".format( 
        mongodb_conf["atlas_user"], mongodb_conf["atlas_cstr"] ))
    
    
    client = pymongo.MongoClient(conn_str)

db = client[mongodb_conf["dbname"]]
collection=db[mongodb_conf["dbname"]]

    
def generate_connection(mongodb_conf):
    if not mongodb_conf["atlas"]:
        # normal mongodb server (local or remote)
        conn_str = "mongodb://" + mongodb_conf["host"] + ":" + str(mongodb_conf["port"]) + "/"    
        print(" ... setting it up for mongoDB: " + conn_str)
        client = pymongo.MongoClient(mongodb_conf["host"], mongodb_conf["port"])
        #db = client[mongodb_conf["dbname"]]
        #collection=db[mongodb_conf["dbname"]]

    else:
        # go cloudy &  set it up for atlas use
        if not mongodb_conf["urlencode"]:
            conn_str = mongodb_conf["atlas_cstr"]
            print(" ... setting it up for mongoDB Atlas: {}".format( conn_str[conn_str.index(r"@"):] ))
        else:
            conn_str="mongodb+srv://" + urllib.parse.quote(mongodb_conf["atlas_user"]) + ":" 
            conn_str += mongodb_conf["atlas_pwd"] + r"@" + mongodb_conf["atlas_cstr"]
            print(" ... setting it up for mongoDB Atlas: ({}) @{} ".format( 
            mongodb_conf["atlas_user"], mongodb_conf["atlas_cstr"] ))
        
        
        client = pymongo.MongoClient(conn_str)

    db = client[mongodb_conf["dbname"]]
    collection=db[mongodb_conf["dbname"]]
    import collections
    dbinfo = collections.namedtuple('db_info', 'db_collection')
    return dbinfo(db, collection)