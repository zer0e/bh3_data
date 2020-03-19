# bh3_data
本项目爬取游戏崩坏3中的部分数据，包括武器，圣痕，补给等。数据来源于[月光社](http://3rdguide.com/)中的武器，圣痕，战场作业三个数据，和[官方补给公示](https://www.bh3.com/news/gacha)中的补给数据

# Dependency 
- requests
- pymysql(可选)
# Usage
0. 使用每个脚本前，如需将数据存放于数据库，则修改脚本中的if_use_sql，并修改脚本中mysql的host，username与password，并提前建立好数据库，导入sql文件。  
1. 其中武器与圣痕可以在脚本中选择是否下载图片。
2. 执行完成后，可以使用toexcel.py将json数据转换成excel文件。
3. 补给数据使用方法详见补给中的README

# About
**本项目仅供学习交流使用**