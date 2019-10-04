import tornado.ioloop
import tornado.web
from redmonty.handlers.powhandler import PowHandler
from redmonty.application import app, route
from redmonty.models.redis.redisinfo import Redisinfo
from redmonty.models.tinydb.connections import Connections
import simplejson as json

# ROUTING:
# You can decorate routes on the handler classes or on the methods directly.
# 
# You can use flask/werkzeug style routing.
#      example: @app.add_route('/test/<uuid:identifier>', dispatch={"get" : "testuuid"})
# Or you can use regex in the routes as well:
#      example: @route('/test/([0-9]+)', dispatch=["get"] )
#      any regex goes. any group () will be handed to the handler 
#      see example handler below.
# 
# Check the docs for more info: https://www.pythononwheels.org/documentation
#

@app.add_route(r"/", dispatch={"get" : "index"}, pos=1)
#@app.add_route(r"/index/([0-9]+)", dispatch={"get" : "index_identifier", "params" : ["identifier"] })
@app.make_routes()
class IndexdHandler(PowHandler):
    def index(self, year=None):
        """
            Example Method with class attached routing (see above "/" )
        """
        print(" Calling IndexHandler.index from handlers/shorties.py: parameter index: " + str(year))
        conn = self.get_secure_cookie("redisui:current_connection", None)
        print(f"found existing connnection cookie: {str(conn)}")
        if conn:
            c=Connections()
            redis_conf=c.find(c.where("_uuid") == id)
            self.render("redisdash.tmpl", connected=True, connection_id=conn, connection=redis_conf)
        else:
            #self.set_secure_cookie("current_connection", "None")
            self.redirect("/connections_list")
    
    @route(r'/serverinfo/<uuid:id>', dispatch=["get"])
    def serverinfo(self, id):
        """
            render the server info view for the connection 
            with the given uuid
        """
        r=Redisinfo()
        c=Connections()
        redis_conf=c.find(c.where("_uuid") == id)
        r.set_connection(redis_conf=redis_conf.to_dict())
        print(json.dumps(r.db.info()))
        try:
            self.render("serverinfo.tmpl", connected=True, connection_id=id, info=r.db.info())
        except:
            self.error(message="Could not connect to Redis DB", data=json.dumps(redis_conf))
        

    @route(r'/index/<uuid:identifier>', dispatch=["get"])
    def index_uuid(self, identifier=None):
        """
            Example method with Method attached route and Flask style route
        """
        print(" Calling Indexhandler.tetuuid Indentifier: {}".format(str(identifier)))
        self.write("uuid: " + str(identifier))
    
    @route(r"/index/([0-9]+)", dispatch=["get"], params=["identifier"])
    def index_identifier(self, identifier=None):
        """
            Example method with Method attached route and tornado/regex style route
        """
        print(" Calling Indexhandler.get_story Indentifier: {}".format(str(identifier)))
        self.write("int: " + str(identifier))



@app.make_routes()
class PyTestHandler(PowHandler):
    @route(r"/testresults", dispatch=["get"])
    def show_results(self):
        """
            this action will show the pytest from test/runtests.py 
        """
        self.render("testreport.html")
    
    @route(r'/test/<uuid:identifier>', dispatch=["get"])
    def testuuid(self, identifier=None):
        """
            Example method with Method attached route and Flask style route
        """
        print(" Calling Indexhandler.tetuuid Indentifier: {}, format: {}".format(str(identifier)))
        self.render("index.tmpl")
    
    @route(r'/test/<int:val>', dispatch=["get"])
    def testintval(self, val=None):
        """
            Testcase: dont delete (see tests/run_tests.py)
        """
        self.write(str(val))
    
# this will be the last route since it has the lowest pos.
@app.add_route(r".*", pos=0)
class ErrorHandler(PowHandler):
    def get(self):
        return self.error( template="404.tmpl", http_status=404  )


