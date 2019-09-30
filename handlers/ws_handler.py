#
# websocket for RedisUI.py
# 

#from tornado.websocket import WebSocketHandler
from handlers.powwshandler import PowWsHandler
import simplejson as json
from redmonty.models.redis.redisinfo import Redisinfo
from redmonty.models.tinydb.connections import Connections
import datetime
from redmonty.config import myapp, redisui

class EchoWebSocket(PowWsHandler):

    def __init__(self, *args, **kwargs):
        """ init some internal stuff     """
        super().__init__(*args, **kwargs)
        self.redisclients={}

    def open(self):
        print("WebSocket opened...")

    def get_client(self,clientID):
        """
            returns the client for the given clientID
            or creates a new one
        """
        c=self.redisclients.get(clientID, None)
        if c:
            return c
        else:
            return Redisclient()
    def remove_client(self, clientID=None):
        """
            remove a client from the list.
            Return dict[clientID]
            or None (if failed or not in the list)
        """
        return self.redisclients.pop(clientID, None)

    def on_message(self, message):
        """ dispatch by method """
        print("received: " +  str(message))
        data = json.loads(message)
        try:   
            f = getattr(self, data.pop("method"), None)
            if callable(f):
                # call the given method
                result = f(data)
            
            if result:
                self.write_message(result)
        except Exception as e:
            data = {
                "method"    :   "dispatcher",
                "type"      :   "error",
                "data"      :   str(e)
            }
            self.write_message(json.dumps(data))
    
    def welcome(self, message):
        """ 
            try to register the client
            and return the info message
        """
        try:
            connection_id = message["connection_id"]
            r=Redisinfo()
            # get the connection from the DB 
            print(f"connecting to: {connection_id}")
            c=Connections()
            redis_conf=c.find(c.where("_uuid") == connection_id)
            r.set_connection(redis_conf=redis_conf.to_dict())
            try:
                result = r.db.ping()
                client_id = message["client_id"]
                if not client_id in self.redisclients:
                    self.redisclients[client_id] = r
                data = {
                    "method"    :   "welcome",
                    "type"      :   "info",
                    "data"      :   r.db.info()
                }
            except Exception as e:
                print(str(e))
                data = {
                    "method"        :   "welcome",
                    "type"          :   "error",
                    "message"       :   "Could not connect to host...",
                    "redirect"      :   True,
                    "redirect_url"  :   "/connections_list",
                    "data"          :   "Nothing"
                }
            return json.dumps(data)

        except Exception as e:
            data = {
                "method"    :   "welcome",
                "type"      :   "error",
                "data"      :   str(e)
            }
            return json.dumps(data)
    
    def scan(self, message):
        """ 
            scan db keys and return the result 
        """
        r=self.get_client(message["client_id"])
        
        result=r.db.scan(message["data"]["cursor"], match=message["data"]["data"]+"*", count=redisui["scan_max"])
        print(f"scanning: ...cursor={message['data']['cursor']} match={message['data']} : {str(result)}")
        data = {
                "method"    :   "scan",
                "type"      :   "scan",
                "data"      :   result
            }
        return json.dumps(data)
    
    def cli(self, message):
        """ 
            scan db keys and return the result 
        """
        try:
            r=self.get_client(message["client_id"])
            print(f"executing: ... {message['data']} ")
            result=r.db.execute_command( message["data"] )
        except Exception as e:
            result=str(e)
        data = {
                "method"    :   "cli",
                "type"      :   "cli",
                "data"      :   result
            }
        return json.dumps(data)
    
    def disconnect(self, message):
        """ 
            remove the connection for this
            clientID from the connection list.
            Remember. A connection pool is used so there is no
            need to really low_level disconnect.
        """
        r=self.remove_client(message["client_id"])        
        r=True
        if r:
            print(f"disconnecting: ...: client_id: {message['client_id']}, connection_id: {message['data']}  ")
        else:
            print(f"Error disconnecting: ...: client_id: {message['client_id']}, connection_id: {message['data']}  ")
        data = {
                "method"    :   "disconnect",
                "type"      :   "disconnect",
                "data"      :   "/connections_list"
            }
        return json.dumps(data)

    def getval(self, message):
        """ 
            scan db keys and return the result 
        """
        r=self.get_client(message["client_id"])
        result=r.db.get(message["data"])
        print(f"get: ...: {message['data']} : {str(result)}")
        print(type(result))
        try:
            result=json.loads(str(result))
        except Exception as e:
            result=str(e)
        data = {
                "method"    :   "getval",
                "type"      :   "getval",
                "data"      :   result
            }
        return json.dumps(data)
    
    def delete(self, message):
        """ 
            delete the key and value from the db
        """
        r=self.get_client(message["client_id"])
        result=r.db.delete(message['data']['key'])
        print(f"deleted: ...: {message['data']['key']} : {str(result)}")
        
        #try:
        #    result=json.loads(str(result))
        #except Exception as e:
        #    result=str(e)
        data = {
                "method"    :   "delete",
                "type"      :   "delete",
                "data"      :   result
            }
        return json.dumps(data)

    def create(self, message):
        """ 
            create the new key, value pair
        """
        r=self.get_client(message["client_id"])
        #r.init_from_dict( message["data"]["value"])
        print(f'create:  {message["data"]["value"]}')
        data=json.loads(message["data"]["value"])
        result=r.db.set(message["data"]["key"], json.dumps(data))
        #result=r.upsert_set()
        print(f"set: ...: {message['data']['key']} : {message['data']['value']}")
        if result:
            message="Created {} successfully".format(message["data"]["key"])
        data = {
                "method"    :   "create",
                "type"      :   "create",
                "message"   :   message,
                "data"      :   result
            }
        return json.dumps(data)
    
    def update(self, message):
        """ 
            update the value for the given key.

        """
        r=self.get_client(message["client_id"])
        #r.init_from_dict( message["data"]["value"])
        print(f'update:  {message["data"]["value"]}')
        data=json.loads(message["data"]["value"])
        result=r.db.set(message["data"]["key"], json.dumps(data))
        #result=r.upsert_set()
        print(f"set: ...: {message['data']['key']} : {message['data']['value']}")
        if result:
            message="Update for {} successfull".format(message["data"]["key"])
        data = {
                "method"    :   "update",
                "type"      :   "update",
                "message"   :   message,
                "data"      :   result
            }
        return json.dumps(data)

    def echo(self, message):
        """ send the info welcome reply       """
        
        data = {
                "method"    :   "echo",
                "type"      :   "info",
                "data"      :  json.dumps(r.db.info())
            }
        return json.dumps(data)
        
    def on_close(self):
        print("WebSocket closed")
