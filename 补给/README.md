# 崩坏3补给数据可视化  
支持扩充，精准A，精准B补给的出货量统计，数据来源于崩坏3官方补给公示

# Dependency 
- requests
- pymysql 
- matplotlib(可选)

# Usage   
python main.py {get,analysis,delete} [-t number] [-n name] [-p ]   

0. 修改lib.py中的mysql的用户名，密码，数据库，导入sql文件
1. python main.py get 10 爬取10次官网公示详情  
2. python main.py analysis {扩充,精准A,精准B} -p 获取该补给详情，并使用饼图分析百分比 
3. python main.py delete 清空数据库数据

# About
由于官方公示中并没有给出补给具体时间，并且个人猜测公示中的补给是随机出现的，所以本人定义了间隔5分钟时间，所以可能出现重复出货未统计或者重复统计的情况，数据仅供参考。  
**本项目仅供学习交流使用**