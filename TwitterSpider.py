import re
import urllib
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import urllib3
import time
import random
from header import headers_list


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

urllib3.disable_warnings()  # 忽略https证书告警
# desktop user-agent

def search(resultFolder,query,itemnum):
    query = query.replace(' ', '+')
    result_list = []
    result_number = 0
    
    legalname = query = query.replace('/', 'and')
    file = "./"+resultFolder+"/"+f"{legalname}.xlsx"
    workbook = xlsxwriter.Workbook(file)
    table_name = 'sheet1' 
    worksheet = workbook.add_worksheet(table_name) 
    urlresults = []
    num = 1
    while(num<itemnum+1):
        try:        
            URL = f"https://www.google.com.hk/search?q={query}&newwindow=1&ei=MSEaYcmdH9TW-QaTr7aIBg&start={num}&sa=N&ved=2ahUKEwiJ-vanj7XyAhVUa94KHZOXDWE4FBDw0wN6BAgBEEU&biw=1366&bih=773"
            headers = {"user-agent": USER_AGENT}

            #headers = random.choice(headers_list)
            proxies = {'http':'http://127.0.0.1:7890'}
            resp = requests.get(URL, headers=headers, verify=False,proxies=proxies)
            time.sleep(5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")

                # 得到基本的搜索条目数量
                # <div id="result-stats">Page 2 of about 32,200,000 results<nobr> 
                # (0.34 seconds)&nbsp;</nobr></div>
                if num==0:
                    results = soup.find_all(attrs={'id':'result-stats'})
                    for result in results:
                        if hasattr(result,'text'):
                            result_num = result.text
                            if result_num is None:
                                continue
                            num_ = result_num.split(' ')
                            print('result_num:',num_[1])
                            worksheet.write(0, 1,  num_[1]) 
                            worksheet.write(0, 2,  'title') 
                            worksheet.write(0, 3,  'abstract') 
                            worksheet.write(0, 4,   'urls') 


                # url在<div>标签下的<a>标签下的href值里
                # 从url节点开始找title信息和abstract信息
                

                for g in soup.find_all('div'):  # <div>
                    anchors = g.find_all('a')  # <a href="">
                    if anchors:
                        for i in range(len(anchors)):
                            if hasattr(anchors[i],'attrs') and 'href' in anchors[i].attrs:
                                link = anchors[i].attrs['href']  # 提取字典内容
                                if link is None:
                                    continue
                                # 正则过滤URL，删除掉一些乱码
                                if re.match('/', link) is None and re.match('(.*)google.com',
                                    link) is None and link != '#' and link.find(
                                    'search?q') == -1:
                                    # 过滤掉重复的URL
                                    flag = True
                                    for res in urlresults:
                                        if res.split(".site")[0] == link.split(".site")[0]:
                                            flag = False
                                    if link in urlresults:
                                        flag = False
                                        continue
                                    if flag:
                                        #利用url节点找到对应的标题和摘要
                                        #print(link)
                                        goodurlNode = anchors[i]
                                        titlenode = goodurlNode.find('h3')
                                        if titlenode is None:
                                            continue
                                        grandp = goodurlNode.parent.parent
                                        asbtractNodes = grandp.next_sibling
                                        if asbtractNodes is not None:
                                            text = asbtractNodes.children
                                            for i,child in enumerate(asbtractNodes):
                                                mytext = child.text
                                                if mytext is None:
                                                    continue
                                                urlresults.append(link)
                                                result_list.append([titlenode.text,mytext,link])

            # 每爬一页写入一次文件
            for res in result_list:
                result_number += 1
                worksheet.write(result_number, 0, " ") 
                worksheet.write(result_number, 1,  res[0])
                worksheet.write(result_number, 2,  res[1])
                worksheet.write(result_number, 3,  res[2])

            print('items:',num,' is recorded')
            num += 8
        except:
            print('重试')
    workbook.close()
