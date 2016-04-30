# Step By Step For Your Task

## Task on Analysis Server

#### 1 Add your task module 

reference: ``` /analysis_task/demo_turbine```  exactly

    set your task module name

    coding your task file.

for examle your task:  m301test

```
analysis_task
     |
     |--m300test
         |
         |--readme.txt: your task introduction
         |
         |--__init__.py  :  module
         |
         |--ana.py : task analysis code
         |
         |--tag_in.txt: input tag of your task (utf-8)
         |
         |--tag_out.txt: input tag of your task (utf-8)
         |
         |--sampling_simulation.py： sampling simulation on tag_in.txt to redis
         |
         |--online_analysis.py：
                                    
                                     class yourtask:
                                    
                                     online_analysis based on 
                                            tag_in.txt
                                            tag_out.txt
                                            ana.py
                                     1) get tag in/out info from  tag_in.txt & tag_out.txt   
                                     2) get real-time from redis
                                     3) analysis by ana.py
                                     4) put result to redis
 
```
 
add your module to
 
/analysis_task/__init__.py
```python
from analysis_task.demo_turbine import *
 
# add your module here

from analysis_task.m300test import *

```

#### 2  Add your task to Simulation and Analysis thread

for examle your task:  m300test

/analysis_thread/sampling_simulation_thread_runner.py

```python
     
    taginfile = os.path.join(analysis_taskpath, "m300test", "tag_in.txt")
    
    Simulation = yourtaskSimulation(taginfile)
    TaskList.append(Simulation)
```    


/analysis_thread/online_analysis_thread_runner.py

```python
    taginfile = os.path.join(analysis_taskpath, "m300test", "tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "m300test", "tag_out.txt")
  
     # your task class :yourtask
    task = yourtask(taginfile, tagoutfile) 
    TaskList.append(task)
```    

#### 3 Test your task 
    
    3.1 Redis Server On
    
    3.2 sampling_simulation_thread_runner.py
    
    3.3 online_analysis_thread_runner.py

## Task on WWW Server

### 1 Add your task user page

####  1  page templates: 

 www/templates/m300test_ui.html 
  
 ```javascript 
 <script type="text/javascript"> 
     ws = new WebSocket("ws://" + window.location.host + "/m300test_websocket");
 </script>
```    
#### 2  page handler: 

 www/handler/m300test_handler.py  
    
 www/handler/m300test_tag.txt (utf-8)
     
```python    
   
    class initHandler(tornado.web.RequestHandler):

         def get(self):
        
            tagfile = "./handler/m300test_tag.txt"
  
            self.render("m300test_ui.html", title=title, tagname=taglist)
```
    
 
#### 3  WWW 

www/__init__.py
    
    from www.handler.m300test_handler import *
  
 www/app.py
    
 ```python  
     
     import www.handler.m300test_handler as m300test
     
     handlers = [
           
            (r"/", indexHandler),
           
            # demo handler
            (r"/demo_tb/", demo_tb.initHandler),
            (r"/demo_tbwebsocket", demo_tb.WebSocketHandler),
            
            # add your handler，： 
            (r"/m300test/", m300test.initHandler),
            (r"/m300test_websocket", m300test.WebSocketHandler),
            
            
        ]
```

www/templates/index.html

```html
 <div class="container">
        <h3 class="offset3">分析任务 </h1>
        <ul class="pull-center">
	      <li><a href="/demo_tb/">示例:高压缸效率</a></li>
         
          <!-- add your link  --> 
         <li><a href="/m300test/">m300test</a></li>   
    
        </ul>
 </div>
````