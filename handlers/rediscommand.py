#from redmonty.handlers.base import BaseHandler
from redmonty.handlers.powhandler import PowHandler
from redmonty.models.tinydb.rediscommand import Rediscommand as Model
from redmonty.config import myapp, database
from redmonty.application import app
import simplejson as json
import tornado.web

@app.add_rest_routes("rediscommand")
class Rediscommand(PowHandler):
    """
    every pow handler automatically gets these RESTful routes
    when you add the : app.add_rest_routes() decorator.
    
    1  GET    /rediscommand                           #=> list
    2  GET    /rediscommand/<uuid:identifier>         #=> show
    3  GET    /rediscommand/new                       #=> new
    4  GET    /rediscommand/<uuid:identifier>/edit    #=> edit 
    5  GET    /rediscommand/page/<uuid:identifier>    #=> page
    6  GET    /rediscommand/search                    #=> search
    7  PUT    /rediscommand/<uuid:identifier>         #=> update
    8  PUT    /rediscommand                           #=> update (You have to send the id as json payload)
    9  POST   /rediscommand                           #=> create
    10 DELETE /rediscommand/<uuid:identifier>         #=> destroy
    
    Standard supported http methods are:
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    handler.

    curl tests:
    for windows: (the quotes need to be escape in cmd.exe)
      (You must generate a post model andf handler first... update the db...)
      POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first rediscommand\" }" http://localhost:8080/rediscommand
      GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/rediscommand
      PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/rediscommand
      DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/rediscommand
    """
    model=Model()
    
    # these fields will be hidden by scaffolded views:
    hide_list=["id", "created_at", "last_updated"]

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="rediscommand show", data=res)
        
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="rediscommand, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="rediscommand page: #" +str(page), data=res )  
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="rediscommand, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="rediscommand, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="rediscommand, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="rediscommand, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="rediscommand, error updating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        res = m.find_by_id(id)
        res.init_from_json(data_json, simple_conversion=True)
        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="rediscommand, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="rediscommand, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



    @tornado.web.authenticated
    def destroy(self, id=None):
        try:
            data_json = self.request.body
            print("  .. DELETE Data: ID:" + str(data_json))
            m=Model()
            m.init_from_json(data_json)
            res = m.find_by_id(m.id)
            res.delete()
            self.success(message="rediscommand, destroy id: " + str(m.id))
        except Exception as e:
            self.error(message="rediscommand, destroy id: " + str(e))
    
    def search(self):
        m=Model()
        return self.error(message="rediscommand search: not implemented yet ")