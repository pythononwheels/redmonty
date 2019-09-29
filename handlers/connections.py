#from redmonty.handlers.base import BaseHandler
from redmonty.handlers.powhandler import PowHandler
from redmonty.models.tinydb.connections import Connections as Model
from redmonty.config import myapp, database
from redmonty.application import app, route
import simplejson as json
import tornado.web

@app.make_routes()
@app.add_rest_routes("connections")
class Connections(PowHandler):
    """
    every pow handler automatically gets these RESTful routes
    when you add the : app.add_rest_routes() decorator.
    
    1  GET    /connections                           #=> list
    2  GET    /connections/<uuid:identifier>         #=> show
    3  GET    /connections/new                       #=> new
    4  GET    /connections/<uuid:identifier>/edit    #=> edit 
    5  GET    /connections/page/<uuid:identifier>    #=> page
    6  GET    /connections/search                    #=> search
    7  PUT    /connections/<uuid:identifier>         #=> update
    8  PUT    /connections                           #=> update (You have to send the id as json payload)
    9  POST   /connections                           #=> create
    10 DELETE /connections/<uuid:identifier>         #=> destroy
    
    Standard supported http methods are:
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    handler.

    curl tests:
    for windows: (the quotes need to be escape in cmd.exe)
      (You must generate a post model andf handler first... update the db...)
      POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first connections\" }" http://localhost:8080/connections
      GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/connections
      PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/connections
      DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/connections
    """
    model=Model()
    
    # these fields will be hidden by scaffolded views:
    hide_list=["id", "created_at", "last_updated"]

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="connections show", data=res)
    
    @route("/connections_list", dispatch=["GET"])
    def list_nice(self):
        m=Model()
        res = m.get_all()  
        # remark: default template will be handler + method => connections_list_nice.tmpl
        self.success(message="connections, index", data=res, connected=False)         

    @route("/connect/<uuid:id>", dispatch=["GET"])
    def connect(self,id=None):
        """  
            connect to the given conncetion ID
            set the according cookie
            and redirect to the dashboard
        """
        if not id:
            self.error(message="No connection ID given")
        else:
            r = self.model.find(self.model.where("id") == id)
            self.set_secure_cookie("redisui:current_connection", str(id))
            if r.type=="redis":
                self.render("redisdash.tmpl", connected=True, connection_id=str(id), show_spinner=True)
            elif r.type == "tinydb":
                self.render("tinydash.tmpl", connected=True, connection_id=str(id), show_spinner=True)
            else:
                msg = "No such connection type"
                print (f"Error connecting : {msg}")
                raise Exception(msg)

    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="connections, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="connections page: #" +str(page), data=res )  
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="connections, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="connections, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="connections, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="connections, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="connections, error updating " + str(m.id) + "msg: " + str(e), 
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
            self.success(message="connections, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="connections, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



    @tornado.web.authenticated
    def destroy(self, id=None):
        try:
            data_json = self.request.body
            print("  .. DELETE Data: ID:" + str(data_json))
            m=Model()
            m.init_from_json(data_json)
            res = m.find_by_id(m.id)
            res.delete()
            self.success(message="connections, successfully deletd id: " + str(m.id), data=str(m.id), format="json")
        except Exception as e:
            self.error(message="connections, destroy id: " + str(e))
    
    def search(self):
        m=Model()
        return self.error(message="connections search: not implemented yet ")