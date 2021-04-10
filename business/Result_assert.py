# -*- coding: utf-8 -*-
'''
Created on 2021年3月14日
@author: cgs
'''
import os.path
import json
import allure
from aspirelibs.logger import logger
from aspirelibs.JSONLibrary import JSONObject
from aspirelibs.DateTimeLibs import TimeUtils
from aspirelibs.cx_oracleLibs import cxOracle
from aspirelibs.redisLibrary import redisHelper
from icecream import ic


class Response_assert(object):
    def assert_json_values(self,Resp_content,kvs):
        json_obj = json.loads(Resp_content)
        for kv in kvs:
            field_info = kv.split("=")
            real_value = JSONObject.get_value_from_json(self,json_obj,field_info[0])[0]
            expect_value = field_info[1]
            assert str(real_value) == str(expect_value) ,"{}的实际结果:【{}】---->>预期结果:【{}】".format(field_info[0],real_value,expect_value)
            allure.attach(("{}的实际结果:【{}】---->>预期结果:【{}】").format(field_info[0],real_value,expect_value))
            logger.info("{}的实际结果:【{}】---->>预期结果:【{}】".format(field_info[0],real_value,expect_value))


class Db_assert(object):
    '''
        数据库断言
    '''
    def assert_db(self,oracle_con,db_assert):
        sqlkvs = db_assert.split('||')
        for sql in sqlkvs:
            list = sql.split('|')
            expect_value,mysql = list
            db = cxOracle(oracle_con)  
            real_value = db.Selectone(mysql)
            assert int(real_value) == int(expect_value),"数据库断言实际结果:【{}】---->>预期结果:【{}】".format(int(real_value),int(expect_value))
            allure.attach(("{}的实际结果:【{}】---->>预期结果:【{}】").format(mysql,int(real_value),int(expect_value)))
            logger.info("数据库断言实际结果:【{}】---->>预期结果:【{}】".format(int(real_value),int(expect_value)))


class Redis_assert(object):
    '''
        数据库断言
    '''
    def assert_redis(self,oracle_con,redis_con,redis_assert):
        sqlkvs = redis_assert.split('||')
        red = redisHelper(redis_con)
        for sql in sqlkvs:
            list = sql.split('|')
            redis,mysql = list         
            db = cxOracle(oracle_con)  
            expect_value = db.Select_one_json(mysql)            
            real_value = red.getStringByKey(redis)
            ic(expect_value)
            ic(real_value)
            assert real_value.lower() == expect_value.lower(),"redis断言实际结果:【{}】---->>预期结果:【{}】".format(real_value.lower(),expect_value.lower())
            allure.attach(("实际结果:【{}】---->>预期结果:【{}】").format(real_value.lower(),expect_value.lower()))
            logger.info("实际结果:【{}】---->>预期结果:【{}】".format(real_value.lower(),expect_value.lower()))


