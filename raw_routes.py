#
# add raw tornado classic routes here:
#

#from handlers.very_raw_own_handler import VeryRawOwnHandler
from handlers.ws_handler import EchoWebSocket
routes = [
            #(r'.*', VeryRawOwnHandler)
            (r"/websocket", EchoWebSocket)
]