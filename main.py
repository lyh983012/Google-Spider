import os
import GoogleSpider
global query

import csv

resultFolder = 'result'
isExists=os.path.exists(resultFolder)
if not isExists:
    os.makedirs(resultFolder) 
    
listOfkey = []
with open("keywords.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        print('searching:',line[0])
        num = GoogleSpider.search(resultFolder,line[0],itemnum=8)
        listOfkey.append([line[0],num])

