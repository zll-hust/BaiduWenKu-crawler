import requests
from selenium import webdriver
from lxml import etree
import re
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import os
from bs4 import BeautifulSoup
import bs4
from docx import Document

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

def parse_type(content):
    return re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]

def parse_txt(html):
    plist = []
    soup = BeautifulSoup(html, "html.parser")
    plist.append(soup.title.string)
    for div in soup.find_all('div', attrs={"class": "bd doc-reader"}):
        plist.extend(div.get_text().split('\n'))
    plist = [c.replace(' ', '') for c in plist]
    plist = [c.replace('\x0c', '') for c in plist]
    return plist

def print_docx(plist, filename):
    file = open(filename + '.txt', 'w',encoding='utf-8')
    for str in plist:
        file.write(str)
        file.write('\n')
    file.close()
    with open(filename + '.txt', encoding='utf-8') as f:
        docu = Document()
        docu.add_paragraph(f.read())
        docu.save(filename + '.docx')

def parse_doc(url, folderPath):
    driver = webdriver.Chrome(r'C:\Users\zll\AppData\Local\Programs\Python\PythonRunSpace\python web crawler\chromedriver.exe')
    driver.get(url)
    # 找到‘继续阅读’按钮  定位至<span class="moreBtn goBtn"><span>还剩35页未读，</span><span class="fc2e">继续阅读</span></span>
    button = driver.find_element_by_xpath("//*[@id='html-reader-go-more']/div[2]/div[1]/span")
    # 按下按钮
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)
    source = re.compile(r'<span class="page-count">/(.*?)</span>')
    number = int(source.findall(driver.page_source)[0])
    # 获取页码数
    # number = total[1]
    time.sleep(1)
    for i in range(2,number):
        driver.find_element_by_class_name("page-input").clear()
        driver.find_element_by_class_name("page-input").send_keys(f'{i}')
        driver.find_element_by_class_name("page-input").send_keys(Keys.ENTER)
        time.sleep(1)
        html=etree.HTML(driver.page_source)
        # 找到picture容器
        links=html.xpath("//div[@class='reader-pic-item']/@style")
        # 找到图片对应的url
        part = re.compile(r'url[(](.*?)[)]')
        qa="".join(links)
        z=part.findall(qa)
        if i == 2:
            for m in range(3):
                pic = requests.get(z[m]).content
                with open(f'./照片/{m+1}.jpg','wb') as f:
                    f.write(pic)
                    f.close()
        else:
            pic = requests.get(z[2]).content
            with open(f'./照片/{i+1}.jpg','wb') as f:
                f.write(pic)
                f.close()
        time.sleep(1)
    driver.quit()

def parse_other(url, folderPath):
    driver = webdriver.Chrome(r'C:\Users\zll\AppData\Local\Programs\Python\PythonRunSpace\python web crawler\chromedriver.exe')
    driver.get(url)
    # 找到‘继续阅读’按钮  定位至<span class="moreBtn goBtn"><span>还剩35页未读，</span><span class="fc2e">继续阅读</span></span>
    button = driver.find_element_by_xpath("//*[@id='html-reader-go-more']/div[2]/div[1]/span")
    # 按下按钮
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)
    source = re.compile(r'<span class="page-count">/(.*?)</span>')
    number = int(source.findall(driver.page_source)[0])
    # 获取页码数
    # number = total[1]
    time.sleep(1)
    # 获取图片
    for i in range(2,number):
        driver.find_element_by_class_name("page-input").clear()
        driver.find_element_by_class_name("page-input").send_keys(f'{i}')
        driver.find_element_by_class_name("page-input").send_keys(Keys.ENTER)
        time.sleep(1)
        html=etree.HTML(driver.page_source)
        # 找到picture容器"//div[@class='reader-pic-item']/@style"
        z=html.xpath('//div[@class="ppt-image-wrap"]/img/@src')
        # print(z)
        # 保存图片
        if i == 2:
            for m in range(3):
                pic = requests.get(z[m]).content
                with open(folderPath + f'/{m + 1}.jpg','wb') as f:
                    f.write(pic)
                    f.close()
        else:
            pic = requests.get(z[i]).content
            with open(folderPath + f'/{i + 1}.jpg','wb') as f:
                f.write(pic)
                f.close()
        time.sleep(1)
    driver.quit()


def print_pdf(folderPath, filename):
    files = os.listdir(folderPath)
    jpgFiles = []
    sources = []
    for file in files:
        if 'jpg' in file:
            jpgFiles.append(file)
    tep = []
    for i in jpgFiles:
        ex = i.split('.')
        tep.append(int(ex[0]))
    tep.sort()
    jpgFiles=[folderPath +'/'+ str(i) + '.jpg' for i in tep]
    output = Image.open(jpgFiles[0])
    jpgFiles.pop(0)
    for file in jpgFiles:
        img = Image.open(file)
        img = img.convert("P")
        sources.append(img)
    output.save(f"./{filename}.pdf","PDF",save_all=True,append_images=sources)

def main():
    # txt:
    # url = 'https://wenku.baidu.com/view/4e29e5a730126edb6f1aff00bed5b9f3f90f72e7.html?rec_flag=default'
    # ppt:
    # url = 'https://wenku.baidu.com/view/5422888649649b6648d747f8.html?fr=search'
    # doc:
    # url = 'https://wenku.baidu.com/view/7ae14c96910ef12d2af9e7c9.html'
    # pdf:
    # url = 'https://wenku.baidu.com/view/5292b2bc0166f5335a8102d276a20029bd64638c.html?fr=search'
    
    url = 'https://wenku.baidu.com/view/a4ac1b57dd88d0d232d46a0f.html?fr=search'
    ticks = time.time()
    filepath = './照片' + str(ticks)
    filename = 'test'
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    html = getHTMLText(url)
    type = parse_type(html)
    # 当你要爬取文本文档时，打开下列注释
    # type = 'txt'
    print(type)
    if type == 'txt' :
        plist = parse_txt(html)
        print_docx(plist, filename)
    elif type == 'doc' or type == 'pdf':
        parse_doc(url, filepath)
        print_pdf(filepath , filename)
    else:
        parse_other(url, filepath)
        print_pdf(filepath, filename)
    print('恭喜你，任务已经完成！')

if __name__ == "__main__":
    main()