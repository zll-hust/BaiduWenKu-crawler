'''
@Description: 
# 计算机程序设计大作业之爬取百度文库内容
# 版本号：version1
# 使用正则表达式爬取百度文库内容（失败）
@Author: zll-hust && xkw
'''

import requests
import re

headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}

def getHTMLText(url):
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        else:
            print('获取网页失败')
    except Exception as e:
        print(e)

def parsePage(page): #  'board-index .*?>(\d+)</i>.*?class="name"><.*?>(.*?)</a></p>
    items = re.findall('<title>人教版八年级上册第五单元(.*?)教案8&nbsp;- 百度文库</title>',page,re.S)
    print(items)
    return items

url = 'https://wenku.baidu.com/view/4e29e5a730126edb6f1aff00bed5b9f3f90f72e7.html?rec_flag=default'
html = getHTMLText(url)
datas = parsePage(html)