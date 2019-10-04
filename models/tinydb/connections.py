#
# TinyDB Model:  Connections
#
from redmonty.models.tinydb.tinymodel import TinyModel

class Connections(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        "type"      :   { "type" : "string", "allowed" : ["redis", "tinydb"], "default" : "redis"},
        'dbname'    :   { 'type' : 'string' },
        'host'      :   { 'type' : 'string', "default" : "localhost" },
        'port'      :   { 'type' : 'integer', "default" : 6379 },
        'user'      :   { 'type' : 'string'},
        "passwd"    :   { 'type' : 'string', "default" : "" },
        "strict"    :   { "type" : "boolean", "default" : True}
        }

    
    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]
    
    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    
    #
    # your model's methods down here
    #
