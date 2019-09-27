
![redmonty logo](http://www.pythononwheels.org/static/upload/redmonty_logo_2.png)


# redmonty is a simple web based UI for REDis, MONgoDB and TinYDB based on python.

> Opensource and free. 

## Based on 
* Tornado(PythonOnWheels)
* Websockets


## Installation

> Just clone the repo and start the server.

## Status so far 
### Redis working 
* Connect
* Scan keys by pattern
* Create (set)
* Read (get)
* Update
* Delete
* Server info

![redmonty usage](http://www.pythononwheels.org/static/upload/redmonty_usage_gif_1.gif)

## Next steps

* Add Hash Set/Get for Redis
* Add tinyDB
* Add mongoDB
* make client multi connect
** one channel per connection 

Since PythonOnWheels supports mongoDB and tinyDB out of the box and they also support
JSON Documents, they can use the same UI as already implemented for Redis.
Just the Connection and CRUD methods need to be adapted

## For more info check: [The Homepage](http://www.pythononwheels.org/redmonty)


    