#
# base connection for TinyDB 
#
from redmonty.config import database
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from redmonty.models.tinydb.serializer import DateTimeSerializer

    
def generate_connection(tinydb_conf=None):
    """
        create a connection from th given conf
        or from config.py (if tinydb_conf == None)
    """
    if tinydb_conf == None:
        tinydb = database.get("tinydb", None)        
    else:
        tinydb = tinydb_conf
    
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

    if tinydb:
        conn_str = tinydb["dbname"]
        print(" ... setting it up for tinyDB: " + conn_str)
        return TinyDB(conn_str, storage=serialization)
    else:
        raise Exception("I had a problem setting up tinyDB")
    
    