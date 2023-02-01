import os
import GoogleSpider
global query

import csv

resultFolder = 'result'
isExists=os.path.exists(resultFolder)
if not isExists:
    os.makedirs(resultFolder) 
    
listOfkey = []
ifHasTitleCol = True

with open("keywords_hy.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if ifHasTitleCol:
            ifHasTitleCol = False
            continue 
            
        keywordsAndAddr = line[0]+' '+line[1]
        Specifier = line[4]
        print("Cultural Specifier:",Specifier)
        if 'G' in Specifier:
            keywordsAndAddr += " Greenwich"
        if 'Y' in Specifier:
            keywordsAndAddr += " LGBT"
        print("Now searching: ",keywordsAndAddr)
        num = GoogleSpider.search(resultFolder,keywordsAndAddr,itemnum=24)
        listOfkey.append([line[0],num])

