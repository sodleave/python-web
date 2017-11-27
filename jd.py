# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 19:43:01 2017

@author: user
"""

#import os
from selenium import webdriver
from time import sleep
import datetime  
import time

#os.chdir(ur'C:\Program Files (x86)\Google\Chrome\Application')

#driver=webdriver.Firefox(executable_path='geckodriver.exe')
driver=webdriver.Chrome(executable_path='chromedriver.exe')

def login(uname, pwd):
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
    driver.get("https://cart.jd.com/cart.action")

    driver.find_element_by_link_text("去结算").click()
    now = datetime.datetime.now()
    print('login success:',now.strftime('%Y-%m-%d %H:%M:%S'))
    
def buy_on_time(buytime):
    while True:
        now = datetime.datetime.now()
        if now.strftime('%Y-%m-%d %H:%M:%S') == buytime:
            while True:
                try:
                    driver.find_element_by_id('order-submit').click()
                except Exception as e:
                    time.sleep(0.1)
            print ('purchase success',now.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(0.5)
    
login(u'username', u'passwd')
buy_on_time('2017-11-27 21:39:01')