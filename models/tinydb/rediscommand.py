#
# TinyDB Model:  Rediscommand
#
from redmonty.models.tinydb.tinymodel import TinyModel

class Rediscommand(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'name'      :   { 'type' : 'string', 'maxlength' : 35 },
        'category'  :   { 'type' : 'string' },
        'summary'   :   { 'type' : 'string' },
        "args"      :   { "type" : "list", "default" : []},
        'help_link' :   { 'type' : 'string' },
        "help_text" :   { "type" : "string" }
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
