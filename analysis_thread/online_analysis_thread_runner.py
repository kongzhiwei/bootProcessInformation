# -*- coding: utf-8 -*-
"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""
import os

try:
    from analysis_thread.online_analysis_thread import PeriodAnalysis
except:
    from online_analysis_thread import PeriodAnalysis

try:
    from analysis_task.demo_turbine.task_turbine_online_analysis import UnitHP
except:
    import sys
    sys.path.append("..")
    from analysis_task.demo_turbine.task_turbine_online_analysis import UnitHP


# add your module 
 
if __name__ == "__main__":

    TaskList = []
    
    pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    analysis_taskpath = os.path.join(pardir, "analysis_task")
    
    taginfile = os.path.join(analysis_taskpath, "demo_turbine", "task_turbine_tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "demo_turbine", "task_turbine_tag_out.txt")
    
    DemoUnitHP = UnitHP(taginfile, tagoutfile)
    TaskList.append(DemoUnitHP)
    
    # add you tesk
    
    OnlineTasks = PeriodAnalysis(2, TaskList)
    OnlineTasks.setouttag()
    OnlineTasks.worker()
 
   
