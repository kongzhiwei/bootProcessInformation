# bootProcessInformation

The Prototype Project of  Real-time Monitoring System for Thermal Power Plant

Author:   Cheng Maohua

Email:    cmh@seu.edu.cn

## Dependencies

### Database

    Redis 3.*

### Analysis
	
	Python3.*  
	
	redis-py

	SEUIF97 
	
	https://github.com/Py03013052/SEUIF97

### Web Server

	Tornado 4.*

### Browser

	Support Websocket

## dir

PrototypeRealTimeMonitoring
        |
        |---analysis_task :  Real-time  Monitoring task
        |         |
        |         |--turbine
        |         |
        |         |--boiler
        |         | 
        |
        |---analysis_thread: 
        |
        |---db: redis
        |
        |---doc: documents
        |
        |---www: web werver
             |
             |--handler
             |        |
             |        |--*_handler.py
             |        | 
             |        |--*_tag.txt  
             |        |
             |
             |--static
             |        |--css    
             |        |
             |        |--img
             |        |
             |        |-js  
             |
             |--templates
             |        |
             |        |--*_ui.html
             |        |
             |
             |--app.py：： start web server
             |
               
             