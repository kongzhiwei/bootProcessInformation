# -*- coding: utf-8 -*-
"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""
from analysis_task.turbine.task_turbine_online_analysis import UnitHP

from analysis_thread.online_task_period import PeriodTasks


if __name__ == "__main__":

    TaskList = []
    CurUnitHP = UnitHP('../analysis_task/turbine/task_turbine_tag_in.txt', '../analysis_task/turbine/task_turbine_tag_out.txt')
    TaskList.append(CurUnitHP)
    
    OnlineTasks = PeriodTasks(2, TaskList)
    OnlineTasks.setoutag()
    OnlineTasks.worker()
 
   
