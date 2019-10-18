#
# base connection for Redis 
#
#from redmonty.config import database
import redis
from powlib import Dbinfo
# redis_conf= database.get("redis", None)
# redisdb = None

# if redis_conf:
#     conn_str = " host:{}, port:{}".format(redis_conf["host"], redis_conf["port"])
#     if redis_conf["strict"]:
#         redisdb = redis.StrictRedis(
#                 host=redis_conf["host"], 
#                 port=redis_conf["port"], 
#                 password=redis_conf["passwd"], 
#                 db=redis_conf["dbname"],
#                 decode_responses=True
#             )
#     else:
#         redisdb = redis.Redis(
#                 host=redis_conf["host"], 
#                 port=redis_conf["port"], 
#                 password=redis_conf["passwd"], 
#                 db=redis_conf["dbname"],
#                 decode_responses=True
#             )
#     print(" ... setting it up for RedisDB: " + conn_str )
    
# else:
#     raise Exception("I had a problem setting up RedisDB")

def generate_connection(redis_conf=None):
    if not redis_conf:
        from redmonty.config import database
        redis_conf= database.get("redis", None)
    conn_str = " host:{}, port:{}".format(redis_conf["host"], redis_conf["port"])
    try:
        if redis_conf["strict"]:
            redisdb = redis.StrictRedis(
                    host=redis_conf["host"], 
                    port=redis_conf["port"], 
                    password=redis_conf["passwd"], 
                    db=redis_conf["dbname"],
                    decode_responses=True
                )
        else:
            redisdb = redis.Redis(
                    host=redis_conf["host"], 
                    port=redis_conf["port"], 
                    password=redis_conf["passwd"], 
                    db=redis_conf["dbname"],
                    decode_responses=True
                )
        print(" ... setting it up for RedisDB: " + conn_str )
        print(f"redis ping... {redisdb.ping()}")
        return Dbinfo(db=redisdb, collection=None)
    except:
        raise Exception("I had a problem setting up RedisDB")
