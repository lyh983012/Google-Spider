import os
import GoogleSpider
global query

resultFolder = 'result'
isExists=os.path.exists(resultFolder)
if not isExists:
    os.makedirs(resultFolder) 


query = input("请输入需要搜索的谷歌命令：")
item = int(input("请输入需要爬行的最小项目个数："))

GoogleSpider.search(resultFolder,query,item)

