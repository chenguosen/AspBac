# coding:utf-8

import time

class TimeUtils:
    '''
    14位时间格式，比如20190331102020
    12为时间格式，比如190331102020
    日期和时间,比如2021-03-07 20:57:54
    '''
    
    def get_timestemp(self, strformat = '%Y%m%d%H%M%S'):
        return time.strftime(strformat, time.localtime())

    def get_timestemp12(self, strformat = '%y%m%d%H%M%S'):
        return time.strftime(strformat, time.localtime())
        
    def get_datetime(self,strformat = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(strformat, time.localtime())


if __name__ == '__main__':

    currentTime = TimeUtils().get_timestemp()
    print(currentTime)
    currentTime1 = TimeUtils().get_timestemp12()
    print(currentTime1)
    currentTime2 = TimeUtils().get_datetime()
    print(currentTime2)