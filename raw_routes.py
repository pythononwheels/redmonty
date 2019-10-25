#
# add raw tornado classic routes here:
#

#from handlers.very_raw_own_handler import VeryRawOwnHandler
from handlers.ws_handler import EchoWebSocket
from handlers.ws_tiny_handler import EchoWebSocket_tiny
routes = [
            #(r'.*', VeryRawOwnHandler)
            (r"/websocket", EchoWebSocket),
            (r"/websocket_tiny", EchoWebSocket_tiny)
]