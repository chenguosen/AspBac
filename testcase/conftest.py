'''
Created on 2021年3月14日
@author: cgs
'''
import pytest
import allure
from aspirelibs.cx_oracleLibs import cxOracle
from aspirelibs.redisLibrary import redisHelper
from aspirelibs.logger import logger
from testcase.info import OpenAccount_initsql
from testcase.info import oracle_con
from testcase.info import redis_con
from icecream import ic


@pytest.fixture(scope="module")
def OpenAccount_initdate():

    db = cxOracle(oracle_con)
    db.execute_file(OpenAccount_initsql)
    logger.debug("执行数据库初始化数据{}".format(OpenAccount_initsql))
    allure.attach("{}".format(OpenAccount_initsql), "初始化数据库数据")

    keys = ['BAC_account_userId_900002', 'BAC_user_userId_900002',
            'BAC_BASR_16_9000000000000200002', 'BAC_custom_idEntityNumber_100000002',
            'BAC_account_userId_900003', 'BAC_user_userId_900003',
            'BAC_BASR_16_9000000000000200003', 'BAC_custom_idEntityNumber_100000003',
            'BAC_account_userId_900004', 'BAC_user_userId_900004',
            'BAC_BASR_16_9000000000000200004', 'BAC_custom_idEntityNumber_100000004',
            'BAC_account_userId_900005', 'BAC_user_userId_900005',
            'BAC_BASR_16_9000000000000200005', 'BAC_custom_idEntityNumber_100000005',
            'BAC_account_userId_900006', 'BAC_user_userId_900006',
            'BAC_BASR_16_9000000000000200006', 'BAC_custom_idEntityNumber_100000006']

    dict = {'BAC_account_userId_900004': '{"acctId":310213532,"acctName":"陈国森4","acctSource":"ASPTEST2","acctStatus":1,"acctType":"10","bindMobile":"15818640854","createTime":1615971090349,"identityNumber":"100000004","invalidTime":4102415999000,"userId":"900004","validTime":1615971089000}',
            'BAC_user_userId_900004': '{"acctStatus":1,"createTime":1615910400000,"customId":110213530,"innerUserId":210213531,"userEmail":"qiuhaiyang@139.com","userId":"900004","userMobile":"15818640854","userName":"OCE","userSource":"ASPTEST2","userType":"10"}',
            'BAC_custom_idEntityNumber_100000004': '{"customId":110213530,"customName":"OCE","customType":"10","identityNumber":"100000004"}'
            }

    red = redisHelper(redis_con)
    red.deleteList(keys)
    allure.attach("{}".format(keys), "初始化删除redis数据")

    red.setStringForDict(dict)
    allure.attach("{}".format(dict), "初始化插入redis数据")
