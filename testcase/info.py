'''
Created on 2021年3月14日
@author: cgs
'''
import pytest
from aspirelibs.xlsxLibrary import get_xlsx_data_by_index
from aspirelibs import Config as config
import os

def set_intf_config_dict():

    # 消息模板的存放路径、文件名,接口地址
    i_config_info = {
        "req_templete":["\\testdata\\OpenAccount.rep.json"],
        "case_file":["testdata\\OpenAccount.xlsx"],
        "sql_file":["\\testdata\\init_OpenAccount.sql"],
        "url_path":["/bacservice/OpenAccount"]
        }
    # 结束设置接口配置
    return i_config_info

root_dir = os.path.abspath('.')
Bac_url = config.get_value("Common","ServAddr")
oracle_con = config.get_value("Common","db_conn")
redis_con = config.get_value("Common","redis_conn")
privatekey2 = config.get_value("Common","privatekey2")
case_file_path = set_intf_config_dict().get("case_file")

#账户开户接口
OpenAccount_initsql = root_dir + set_intf_config_dict().get("sql_file")[0]       #获取初始化脚本
case_OpenAccount_data = get_xlsx_data_by_index(case_file_path[0], 0)             #获取账户开户请求用例
case_OpenAccount2_data = get_xlsx_data_by_index(case_file_path[0], 1)            #获取账户开户异常请求用例
req_OpenAccount_file = root_dir + set_intf_config_dict().get("req_templete")[0]  #消息模板
OpenAccount_url = Bac_url + set_intf_config_dict().get("url_path")[0]            #接口地址


