# -*- coding: utf-8 -*-
'''
# Created on 2021-03-07
# @author: cgs
'''
import pytest
import allure
from aspirelibs.JSONLibrary import JSONObject
from aspirelibs.utilLibrary import *
from aspirelibs.RegxLibrary import *
from aspirelibs.logger import logger
from aspirelibs.HttpLibs import Http_Post
from aspirelibs.DsaSingerUtil import DSA_sign
from aspirelibs.cx_oracleLibs import cxOracle
from business.Bac_Reqx import common_biz
from business.Result_assert import Response_assert, Db_assert, Redis_assert
from testcase.info import case_OpenAccount_data, case_OpenAccount2_data, OpenAccount_url, req_OpenAccount_file, oracle_con, privatekey2,redis_con
from icecream import ic
import time

class Test_OpenAccount(object):

    @allure.description("提供账户中心的账户开户，并根据参数提供的产品线和合同编码，自动创建对应账本科目、“产品线+合同编码”与账本科目对应关系、账户账本等功能。开户成功后返回账户ID给调用方。")
    @pytest.mark.parametrize('version,Req_ID,author,case,header,req_parameters,Resp_assert,db_assert,redis_assert', case_OpenAccount_data)
    @allure.title("VerID:{version}|ReqID:{Req_ID}|Author:{author}|CaseTitle:{case}")
    @allure.feature("BDC项目-账户开户请求接口")
    @allure.story("BDC项目-账户开户请求接口正常流功能测试")
    @pytest.mark.testchenguosen33
    def test_normal(self, version, Req_ID, author, case, header, req_parameters, Resp_assert, db_assert,redis_assert, OpenAccount_initdate):

        logger.info("***********************  开始执行用例 *********************** ")
        with allure.step("测试步骤1：准备reqParam信息内容"):
            req_obj = common_biz.load_submitOffersOrder_template(
                self, req_OpenAccount_file)
            allure.attach("{}".format(req_obj), "准备reqParam信息内容")

        with allure.step("测试步骤2：准备测试用例请求报文"):
            if req_parameters != '':
                kvs = match_test_rule_value(req_parameters)
                req_obj = JSONObject.refactoring_json(self, req_obj, kvs)
                req_obj = json.dumps(
                    req_obj, ensure_ascii=False, separators=(',', ':'))
                # reqParam内容进行DSA签名
                sign = DSA_sign(req_obj, privatekey2)
                req_obj = "{\"reqParam\": %s,\"sign\": \"%s\"}" % (
                    req_obj, sign)
                logger.info("请求消息体: {}".format(req_obj))
                allure.attach("{}".format(req_obj), "准备测试用例请求报文")

        with allure.step("测试步骤3：向服务器发送请求并获取响应消息"):
            Resp_code, Resp_content, headers = Http_Post(
                url=OpenAccount_url, data=req_obj.encode("utf-8"), h=eval(header))
            allure.attach("{}".format(OpenAccount_url), "请求URL地址")
            allure.attach("{}".format(Resp_code), "响应码")
            allure.attach("{}".format(Resp_content), "响应消息体")

        with allure.step("测试步骤4：响应消息内容断言"):
            kvs = match_test_rule_value(Resp_assert)
            # 断言Response code
            assert Resp_code == 200
            # 校验响应字段值
            if Resp_assert != '':
                Response_assert.assert_json_values(self, Resp_content, kvs)

        with allure.step("测试步骤5：数据库断言"):
            # 校验数据库
            if db_assert != '':
                Db_assert.assert_db(self, oracle_con, db_assert)
                
        with allure.step("测试步骤6：redis库断言"):
            #校验redis
            if redis_assert != '':
                Redis_assert.assert_redis(self,oracle_con,redis_con,redis_assert)

        logger.info("***********************  结束执行用例 *********************** ")
