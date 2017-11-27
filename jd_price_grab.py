# coding: utf-8
# python+selenium+phantomjs(无界面浏览器)
# JD数据根据输入条件搜索抓取

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import sys
import requests
import re
import urllib2
import time
reload(sys)
sys.setdefaultencoding('utf8')
import json
import csv

def openjd(url,keys):
    #有界面(google浏览器)
    driver = webdriver.Chrome()
    # 无界面()
    #driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs-2.1.1/bin/phantomjs')
    driver.get(url)
    print u'进入..' + driver.title
    #进入页面，找到搜索框
    elem = driver.find_element_by_id('key') #定位到搜索框 赋值
    elem.clear() #清除搜索框数据
    elem.send_keys(u''+keys) #输入数据
    elem.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click() #点击搜索
    sleep(4)
    # 将页面滚动条拖到底部
    js = "var q=document.body.scrollTop=100000"
    driver.execute_script(js)
    #print '下拉scrollTop'
    sleep(1)
    return driver

#匹配数据
def searchJob(driver):
    data = driver.page_source #网页源代码
    #print data
    content = BeautifulSoup(data,'html.parser')
    #匹配具体的详情
    name = content.find_all("div",{"class":"p-name p-name-type-2"}) #商品名称加型号
    i = 1
    for each in name:
        #print '################第' + str(i) + '个商品################'
        productlink = substring(each.a.get("href"))
        if 'http://' == productlink[0:7]:
            #print u"商品详情链接:" + productlink
            listresult.append(productlink)
        #print "\n"
        i +=1
    return driver

def nextPage(driver):
    try:
        driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[4]').click()
        sleep(4)
        # 将页面滚动条拖到底部
        js = "var q=document.body.scrollTop=100000"
        driver.execute_script(js)
        #print '下拉scrollTop2'
        sleep(1)
        # try:
        #     #print driver.page_source
        #     #判断页数是否走完
        #     driver.find_element_by_class_name("pn-next")
        #     print u'有'
        # except WebDriverException:
        #     print u'无'
    except NoSuchElementException:
        print  u'搜索完毕'
        flag = 0
        return flag

#字符串截取对比方法(用来判断链接是否http://不是则补全)
def substring(str):
    str2 = str[0:3]
    if 'http' == str2:
        return str
    else:
        return 'http:'+str

#跳转网页方法
def getHtml2(url):
    html = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8')
    return html
#根据url获得html页面
def getHtml(url):
    page=urllib2.urlopen(url)
    contents=page.read()
    return contents
#数据截取方法  第二个是url链接
def getDetail(soup,each_list):
    question = soup.findAll('div', {'class': 'sku-name'})
    #商品来源
    source = '京东'
    print u'商品来源:'+source
    #品牌
    brand = soup.findAll(id='parameter-brand')
    if len(brand) == 0:
        brand = "空"
        print u'商品品牌:'+brand
    else:
        brand = brand[0].a.get_text()
        print u'商品品牌:'+brand
    #商品全名
    fullname = soup.find('div', {'class': 'sku-name'})
    fullname = fullname.text.strip()
    print u'商品全名:'+fullname
    #商品价格
    #print each_list
    jnumber = 'J_' + re.sub("\D", "", each_list)
    price = requests.post('https://p.3.cn/prices/mgets?type=1&area=172_2799_0&pdtk=& pduid=20170818&pdpin=super_xiaoquan&pin=super_xiaoquan&pdbp=0&skuIds='+jnumber+'& ext=11000000& source =item-pc').text
    price = price[1:-2]
    price = json.loads(price)
    price = price.get('p')
    print u'商品价格:'+price
    #获取时间
    date = time.strftime('%Y%m%d%H%M%S/',time.localtime(time.time()))
    print u'获取时间:'+date
    print '\n'
    data = [(source),(brand),('空'),(fullname),(price),(date)]
    return data
if __name__ == '__main__':
    url = 'http://www.jd.com/'
    keys =raw_input('请输入搜索的关键词:')
    print "请稍等片刻...."
    listresult = []
    num = 1
    driver = openjd(url,keys)
    #总共页数
    s = 1
    try:
        s = driver.find_element_by_class_name('p-skip').text
        s = re.sub("\D", "", s)
    except NoSuchElementException:#页面不存在这个按钮
        print u'只有一页返回页数为1'

    while True:
        print u'##########第'+str(num)+'页信息'
        driver = searchJob(driver)
        flag = nextPage(driver)
        #print flag
        if flag == 0:
            break
        num += 1

        if int(num) > int(s):
            print  u'搜索完毕'
            print '\n'
            break
    driver.close()
    dataresult = []
    for each_list in listresult:
        con = getHtml(each_list)
        soup = BeautifulSoup(con, 'lxml')
        #print each_list
        data = getDetail(soup,each_list)
        #date = time.strftime('%Y%m%d', time.localtime(time.time()))
        dataresult.append(data)
    if len(dataresult):
        with open('test.csv', 'ab') as f:
            writer = csv.writer(f)
            writer.writerows(dataresult)
            print u'写入.csv文件结束'
            f.close()
    else:
            print u'写入.csv文件结束空'