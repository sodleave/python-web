# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:55:49 2017

@author: ly
"""

import os
from selenium import webdriver
from time import sleep
import time

os.chdir(ur'H:\中转站\proj2_miaosha')
driver=webdriver.Chrome(executable_path='chromedriver.exe')

def login(uname, pwd, SPurl):
    driver.get("http://www.jd.com")
    driver.find_element_by_link_text("你好，请登录").click()

    driver.find_element_by_link_text("账户登录").click()
    elem=driver.find_element_by_name("loginname")
    elem.clear()
    elem.send_keys(uname)
    elem=driver.find_element_by_name("nloginpwd")
    elem.clear()
    elem.send_keys(pwd)
    elem=driver.find_element_by_id("loginsubmit").click()
    sleep(4)
    driver.get(SPurl)#wky
    
def buy_on_time():
    while True:
        try:
            driver.find_element_by_xpath("//a[contains(text(),'立即抢购') and @id='btn-reservation']").click()
            sleep(1)
            driver.get("https://cart.jd.com/cart.action")
            driver.find_element_by_link_text("去结算").click()
            driver.find_element_by_id("order-submit").click()
            break
        except Exception as e:
            time.sleep(0.4)
        driver.refresh()
            
username=u'*********'  #用户名
passwd=u'********'  #密码
SPurl=u"https://item.jd.com/4993773.html" #商品地址6043002   4993773
login(username, passwd, SPurl)
buy_on_time()