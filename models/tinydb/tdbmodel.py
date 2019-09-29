#
# TinyDB Model:  Tdbmodel
#
from redmonty.models.tinydb.tinymodel import TinyModel

class Tdbmodel(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = { }

    

    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]
    
    # Toggle to  use the pow schema extensions (id, created_at, last_updated) 
    _use_pow_schema_attrs = False

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    
    #
    # your model's methods down here
    #
