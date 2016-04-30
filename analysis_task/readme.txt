
 分析任务实现模式
 
 所有分析任务实现使用统一的组织形式，都包含同类的6个文件
 
 假设当前任务名为：CurrentName
 
1 任务说明纯文本文件：readme.txt
 
2 数据点纯文本文件2个（utf-8编码）

	计算数据源点； CurrentName_tag_in.txt
	
	计算结果输出点； CurrentName_tag_out.txt
	
3 Python源码

                 数据仿真：CurrentName_sampling_simulation.py -  工作线程
                 
                计算模块： pyCurrentName.py
                
                 在线分析： CurrentName_online_analysis.py
  
 4  运行数据仿真            
 
            由 sampling_simulation_thread_runner.py 将其加入仿真线程列表，启动仿真任务
                            
 5 在线分析任务投入            
 
            由 online_task_thread_runner.py 将其加入任务线程列表，启动分析任务
 
 