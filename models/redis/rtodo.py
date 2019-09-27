#
# Redis Model
#
from redmonty.models.redis.basemodel import RedisBaseModel
from datetime import datetime


class Rtodo(RedisBaseModel):
    #
    # Use the cerberus schema style 
    # which offer you an Elastic schema and
    # immediate validation with cerberus
    #

    # Toggle using the pow schema extensions (id, created_at, last_updated) 
    _use_pow_schema_attrs = False 
    
    schema = {
        'title'     : { 'type': 'string' },
        'text'      : { 'type': 'string', 'maxlength' : 235 },
        'tags'      : { 'type': 'list' },
        'votes'     : { "type": 'integer' }
    }

    #
    # your model's methods down here
    #
    def __init__(self, *args, **kwargs):
        self.init_on_load()