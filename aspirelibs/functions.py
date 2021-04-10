'''
代码重构的定位函数等
'''
from datetime import datetime,date,timedelta
from selenium import webdriver
#以下为driver设置获得1个浏览器对象

driver = webdriver.Firefox(executable_path =r"D:\Python36\geckodriver")

#driver = webdriver.Firefox()
'''
函数 return_driver()的功能是返回driver对象
'''
def return_driver():
    return driver

'''
函数 open_base_site(url)的功能是打开网站web页面
'''
def open_site(url):
    driver.get(url)


#以下为定义函数部分，其目的是返回今天后的第n天的日期，格式为"2019-04-03"
'''
函数date_n(n)将返回n天后的日期
'''
def date_n(n):
    return str((date.today() + timedelta(days = int(n))).strftime("%Y-%m-%d"))
"""
下面的函数是，根据8种selenium定位方法,做二次封装
"""
def id(element):
    return driver.find_element_by_id(element)
def css(element):
    return driver.find_element_by_css_selector(element)
def class_name(element):
    return  driver.find_element_by_class_name(element)
def xpath(element):
    return driver.find_element_by_xpath(element)
"""
函数js通过selenium来执行JavaScript语句
"""
def js(j_s):
    driver.execute_script(j_s)


if __name__ == '__main__':
   print(__name__)