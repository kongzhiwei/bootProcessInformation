
# Step by Step: Social programming 

Social programming Practice based on 

The Prototype Project : Real-time Monitoring System for Thermal Power Plant 

bootProcessInformation: https://github.com/Py03013052/bootProcessInformation

Git Platform: Github.com
 
Development Software: Eclipse CDT, EGIT,PyDev
  
Document Software: Microsoft Visual Code
        
 ```
    One:  Fork bootProcessInformation to your GitHub
    
    Two:  Clone bootProcessInformation to your local 
    
    Three: Import to Eclipse Workspace 
    
    Four: Coding your task 
    
    Five:  Push to your GitHub
    
    Six:  push request and Merge to the base branch
    
   Seven:  sync with the base branch
    
 ```    

## Step One:  Fork dource bootProcessInformation to your gitHub account

Fork source bootProcessInformation

![Fork](./img/1_fork.png)


Forked bootProcessInformation in your GitHub account

![Forked](./img/1_forked.png)


## Step Two:  Clone fored bootProcessInformation to your local  respority

Start clone: git 

![clone_1](./img/2_clone_1.png)

copy url to clipboard
 
![clone_clipboard](./img/2_clone_clipboard.png)

copy source to your local

![clone_source](./img/2_clone_source.png)

Brance selection

![clone_branch](./img/2_clone_branch.png)

cloned respority 

![clone_localgit](./img/2_clone_localgit.png)

## Step Three: Import to Eclipse Workspace 

import to your workspace

File->import

general->Existing  Projects

![workspace](./img/3_workspace.png)

choose your project

![workspace_project](./img/3_workspace_project.png)

imported projects
 
3_workspace_imported.png

![3_workspace_imported](./img/3_workspace_imported.png)

## Step Four: Coding your task 

### 4.1 your analysis_task package 

new pythhon package m300exair

/PrototypeRealTimeMonitoring/analysis_task/m300exair

![4_newpackage.png](./img/4_newpackage.png)


![4_newmodel](./img/4_newmodel.png)

copy all files of  ``analysis_task/demo_turbine``` to your m300exair , rename to


```
analysis_task
     |
     |--m300exair
         |
         |--readme.txt: your task introduction
         |
         |--__init__.py  :  module
         |
         |--pyexair.py : task analysis code
         |
         |--task_exair_tag_in.txt: input tag of your task (utf-8)
         |
         |--task_exair_tag_out.txt: input tag of your task (utf-8)
         |
         |--task_exair_sampling_simulation.py： sampling simulation on task_exair_tag_in.txt to redis
         |
         |--task_exair_online_analysis.py：
 
```

![4_m300exair](./img/4_m300exair.png)


then,coding: 

#### 4.1.1 /analysis_task/__init__.py


```python
# add your module here
from analysis_task.m300exair import *
```

####  4.1.2 pyexair.py

```python
def exaircoff(o2):
    return 21/(21-o2)
```

#### 4.1.3 tag about exair

m300exair/task_exair_tag_in.txt
```
id	desc	defaultvalue
DEMO.DCS2AI.2JZA2226	空预器进口烟气氧量	3.8375
```

m300exair/task_exair_tag_out.txt
```
id	desc defaultvalue
DEMO.DCS2AO.EXAIRCOFF  空预器进口过量空气系数     1.25
```
#### 4.1.4 m300exair/task_exair_online_analysis.py

```python
from datetime import datetime
import codecs

from db.pyredis import TagDefToRedisHashKey, tagvalue_redis, SendToRedisHash
from analysis_task.m300exair.pyexair import exaircoff

class UnitExaircoff:

    def __init__(self, tagin, tagout):
        self.ailist = []
   
        file = codecs.open(tagin, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid}) 
      
    
        self.aolist = []
        file = codecs.open(tagout, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.aolist.append({'id':tagid, 'desc':desc, 'value':None, 'ts':None}) 
 
    def setouttag(self):
        TagDefToRedisHashKey(self.aolist)
 
    def Onlinecal(self):
        o2 = float(self.ailist[0]['value']) 
        cur_exaircoff =exaircoff(o2)
        self.aolist[0]['value'] = cur_exaircoff
    
    def run(self):
        tagvalue_redis(self.ailist)
        self.Onlinecal()
        curtime = datetime.now()
        for tag in self.aolist:
            tag['ts'] = curtime 

        SendToRedisHash(self.aolist)

        tagvalue_redis(self.aolist)
        
        for tag in self.aolist:
            print(tag['desc'], tag['value'])

```

#### 4.1.5 /m300exair/task_exair_sampling_simulation.py

```python
class UnitExaircoffSimulation:

    def __init__(self, tagfile):
        
        self.ailist = []
        file = codecs.open(tagfile, 'r', 'utf-8')
        with file:
            discardline = file.readline()
            for line in  file:
                tagid, desc, value = line.split()
                self.ailist.append({'id':tagid, 'desc':desc, 'value':float(value)}) 
      
        self.o2base = self.ailist[0]['value'] 
  
    def settag(self):
        TagDefToRedisHashKey(self.ailist)
 
    def run(self):
        self.ailist[0]['value'] = self.o2base * (1 + random.random() * 0.005)
        
        curtime = datetime.now()
        for tag in self.ailist:
            tag['ts'] = curtime 
        SendToRedisHash(self.ailist)

        print('UnitExaircoffSimulation sampling on ', self.ailist[0]['value'])

```

### 4.2 your analysis_task to analysis_thread

#### 4.2.1 /analysis_thread/sampling_simulation_thread_runner.py

Add code

```python
try:   
    from analysis_task.m300exair.task_exair_sampling_simulation import UnitExaircoffSimulation
except:
    import sys
    sys.path.append("..")
    from  analysis_task.m300exair.task_exair_sampling_simulation import  UnitExaircoffSimulation
 
  # add you tesk
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    
    Simulation = UnitExaircoffSimulation(taginfile)
    TaskList.append(Simulation)    
```

Test Running

/m300exair/task_exair_sampling_simulation.py

![4_simulation](./img/4_simulation.png)


#### 4.2.2 analysis_thread/online_analysis_thread_runner.py

Add code

```python
# add your module 
try:
    from analysis_task.m300exair.task_exair_online_analysis import UnitExaircoff
except:
    import sys
    sys.path.append("..")
    from analysis_task.m300exair.task_exair_online_analysis import UnitExaircoff
    
     # add your task
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_out.txt")
    
    TaskExaircoff = UnitExaircoff(taginfile, tagoutfile)
    TaskList.append(TaskExaircoff)
```

Test Running

analysis_thread/online_analysis_thread_runner.py

![4_online_analysis](./img/4_online_analysis.png)


### 4.3 your page and handle to www

#### 4.3.1 page handler
 
 copy  demo files and rename to your task,then codeing
 
 handler/m300exair_tag.txt
 ```
 desc	id	si
空预器进口烟气氧量	DEMO.DCS2AI.2JZA2214   %
空预器进口过量空气系数	DEMO.DCS2AO.EXAIRCOFF	/	
 ```

handler/m300exair_handler.py

```python
cur_tag=gentag("./handler/m300exair_tag.txt")
      
class initHandler(tornado.web.RequestHandler):

    def get(self):

        title = '在线监视客户端： 过量空气系数'
        
        cur_tag.GetTagDefInfo()
        tagvalue = cur_tag.TagSnapshot(


```
modifing `www/__init__.py`

```python
 # add your handler
from www.handler.m300exair_handler import *
 
```

#### 4.3.2 page tamplate

copy demo  tamplate and rename for your tash, 


then modifying ```/templates/m300exair_ui.html``` contents


```javascript
 ws = new WebSocket("ws://" + window.location.host + "/m300exair_websocket");
```
 
 #### 4.3.3 add your page tamplate to site
 
 midifing `/www/app.py`
 ```python
 
 try:
    import www.handler.m300exair_handler as m300exair
except:
    import handler.m300exair_handler as m300exair
    
   handlers = [
           
            (r"/", indexHandler),
    
            
            # add your handler，： 
            (r"/m300exair/", m300exair.initHandler),
            (r"/m300exair_websocket",m300exair.WebSocketHandler),
            
        ]   
    
    
 ```
   midifing `templates/index.html`
  ```javascript 
   <div class="container">
        <h3 class="offset3">分析任务 </h1>
        <ul class="pull-center">
	      <li><a href="/demo_tb/">示例：高压缸效率</a></li>
          <!-- add your link  --> 
          <li><a href="/m300exair/">m300exair:过量空气系数</a></li>
            
    
        </ul>
	   </div>
 ```
 #### 4.3.4 Running
 
 `/www/app.py`
 
 Home Page
 
 ![4_index](./img/4_index.png)
 
 your task page
 
![4_page_m300exair](./img/4_page_m300exair.png) 
 
 
## Step Five:  Push to GitHub

### 5.1 commit and push to your fored repository on github

![5_commit_1](./img/5_commit_1.png) 

![5_commit_2](./img/5_commit_2.png) 

check result on github

![5_commit_3](./img/5_commit_3.png)


### 5.2 New pull requests to source repository

![5_pull_1](./img/5_pull_1.png)

Create  pull request

source repository in the left , your repository in the right

request pull your repository (right) to source repository(left)

![5_pull_2](./img/5_pull_2.png)

commit message

![5_pull_3](./img/5_pull_3.png)

## Step Six:  Merge to the base branch(remote/local)

### 6.1 remote merge

check pull requests:

![6_merge_1](./img/6_merge_1.png)

merge pull requests:

![6_merge_2](./img/6_merge_2.png)

![6_merge_3](./img/6_merge_3.png)

### 6.2 source: pull remote  to  local

![6_source_pull_1](./img/6_source_pull_1.png)

![6_source_pull_2](./img/6_source_pull_2.png)

![6_source_pull_3](./img/6_source_pull_3.png)

local after pull

![6_source_pull_4](./img/6_source_pull_4.png)

## Step Seven:  forked branch sync with the source branch

the source branch append guide after your forked, 

sync action: 

7.1 new pull request in your forked branch 

![7_sync_1](./img/7_sync_1.png)

### switching  the  base 

** your forked branch in the left , source repository in the right **

![7_sync_2](./img/7_sync_2.png)

Create　pull request:

note: request pull source branch(right) to your forked branch (left)

![7_sync_30](./img/7_sync_30.png)

![7_sync_3](./img/7_sync_3.png)

you can see all commit in source branch after you forked

![7_sync_31](./img/7_sync_31.png)

pull request +1 :

![7_sync_4](./img/7_sync_4.png)

![7_sync_5](./img/7_sync_5.png)

merge pull request(source branch to your branch)

![7_sync_6](./img/7_sync_6.png)

synced branch

![7_sync_7](./img/7_sync_7.png)