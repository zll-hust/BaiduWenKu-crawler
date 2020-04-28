'''
@Description: 
# 计算机程序设计大作业之爬取百度文库内容
# 版本号：version1(失败)
# 爬取百度文库内ppt内容
@Author: zll-hust && xkw
'''

import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    header = {'User-agent': 'Googlebot'}
    try:
        r = requests.get(url, headers = header, timeout = 30)
        r.raise_for_status()
        r.encoding = 'gbk'
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def findPList(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup.find_all('div', attrs = {"class": "bd doc-reader"}))
    for div in soup.find_all('div', attrs = {"class": "ppt-image-wrap"}):
        url = div.select('img').attrs
        printImg(url)


def printImg(url):
    root=r"./"
    path=root + url.split('/')[-1] + '.jpg'
    try:
        #这一步是防止目标路径不存在
        if not os.path.exists(root):
            os.mkdir(root)
        #判断路径下是否有该张图片
        if not os.path.exists(path):
            header = {'User-agent': 'Baiduspider'}
            r = requests.get(url, headers = header, timeout = 30)
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("爬取失败")

def main():

    url = 'https://wenku.baidu.com/view/605f720f6429647d27284b73f242336c1eb93088.html?fr=search'
    html = getHTMLText(url)
    findPList(html)

main()