from selenium import webdriver
from lxml import etree
import re
from selenium.webdriver.common.keys import Keys
import time
import requests
from PIL import Image
import os

def spider(folderPath):
    # url = 'https://wenku.baidu.com/view/7ae14c96910ef12d2af9e7c9.html'
    url = 'https://wenku.baidu.com/view/5422888649649b6648d747f8.html?fr=search'
    # url = 'https://wenku.baidu.com/view/eac6493bcf2f0066f5335a8102d276a2012960f6.html?fr=search'
    driver = webdriver.Chrome(r'C:\Users\zll\AppData\Local\Programs\Python\PythonRunSpace\python web crawler\chromedriver.exe')
    driver.get(url)

    # 找到‘继续阅读’按钮  定位至<span class="moreBtn goBtn"><span>还剩35页未读，</span><span class="fc2e">继续阅读</span></span>
    button = driver.find_element_by_xpath("//*[@id='html-reader-go-more']/div[2]/div[1]/span")
    # 按下按钮
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)

    # html = etree.HTML(driver.page_source)
    # 找到页码 try处理多种情况
    # try:
    #     try:
    #         try:
    #             page = html.xpath("/html/body/div[16]/div/div/div[2]/div[1]/div/span")
    #             total = page[0].text.split('/')
    #         except:
    #             page = html.xpath("/html/body/div[17]/div/div/div[2]/div[1]/div/span")
    #             total = page[0].text.split('/')
    #     except:
    #         page = html.xpath("/html/body/div[17]/div/div/div[2]/div[1]/div/span")
    #         total = page[0].text.split('/')
    # except:
    #     #/html/body/div[19]/div/div/div[2]/div[1]/div/span
    #     page = html.xpath("/html/body/div[12]/div/div/div[2]/div[1]/div/span")
    #     total = page[0].text.split('/')
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
        # 找到picture容器
        links=html.xpath("//div[@class='reader-pic-item']/@style")
        # 找到图片对应的url
        part = re.compile(r'url[(](.*?)[)]')
        qa="".join(links)
        z=part.findall(qa)
        # 保存图片
        if i == 2:
            for m in range(3):
                pic = requests.get(z[m]).content
                with open(folderPath + f'/{m + 1}.jpg','wb') as f:
                    f.write(pic)
                    f.close()
        else:
            pic = requests.get(z[2]).content
            with open(folderPath + f'/{i + 1}.jpg','wb') as f:
                f.write(pic)
                f.close()
        time.sleep(1)
    driver.quit()

def trans(folderPath, pdf_name):
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
    jpgFiles=[folderPath +'/'+str(i)+'.jpg' for i in tep]
    output = Image.open(jpgFiles[0])
    jpgFiles.pop(0)
    for file in jpgFiles:
        img = Image.open( file)
        img = img.convert("P")
        sources.append(img)
    output.save(pdf_name, "PDF", save_all=True, append_images=sources)

def main():
    # url = input('请输入要爬取的网址')
    # spider("./照片3")
    trans("./照片" , "./test.pdf")
    # combine2Pdf("./照片3/" , "./test.pdf")
    print('恭喜你，任务已经完成！')

if __name__ == '__main__':
    main()