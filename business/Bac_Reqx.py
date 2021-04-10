'''
Created on 2021年3月14日
@author: cgs
'''
from aspirelibs.JSONLibrary import JSONObject
from aspirelibs.DateTimeLibs import TimeUtils
import random
import hashlib
from aspirelibs.logger import logger
from aspirelibs.cx_oracleLibs import *
from datetime import datetime
from aspirelibs.DateTimeLibs import TimeUtils
from aspirelibs.RegxLibrary import *

class common_biz(object):
    '''
        业务逻辑需要根据项目编写
    '''
    def load_submitOffersOrder_template(self, req_template_file):
        req_obj = JSONObject.load_json_from_file(self, req_template_file)
        kvs=[]
        
        #修改json参数值
        reqTime = TimeUtils().get_timestemp()
        kvs.append("$.pubInfo.reqTime" + "=" + str(reqTime))      
        logger.info("重置节点列表：{}".format(kvs))
        print("读取模板的内容为：{}".format(JSONObject.upadate_values_to_json(self, req_obj, kvs)))
        return JSONObject.upadate_values_to_json(self, req_obj, kvs)  
