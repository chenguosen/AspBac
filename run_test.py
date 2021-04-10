# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    run_test
   Author :       cgs
   date：         2020/11/02
-------------------------------------------------
   Change Activity:     2020/11/02
-------------------------------------------------
"""

import pytest
import os


if __name__ == '__main__':
    
   #删除html目录
   os.system('rmdir /s /q html')
   #执行指定文件中，特定类中的特定测试方法,三线程执行用例
   #pytest.main(['testcase/mocp_test/test_serviceOrderQuery.py::Test_serviceOrderQuery::test_normal', '-s', '-v', '-q','-n','3','--alluredir', 'html'])
   #执行指定文件中，特定类中的特定测试方法
   #pytest.main(['testcase/mocp_test/test_submitOffersOrder.py::Test_submitOffersOrder::test_normal', '-s', '-v', '-q', '--alluredir', 'html'])
   #执行指定文件***.py下的所有用例
   #pytest.main(['testcase/mocp_test/test_serviceOrderQuery.py', '-s', '-v', '-q', '--alluredir', 'html'])
   #执行所有被@pytest.mark.slow标记的用例
   pytest.main(['-m','testchenguosen33', '-s', '-v', '-q','--alluredir', 'html'])
   #Pytest命令跟—alluredir参数生成json报告，执行指定文件夹下的所有测试测试用例
   #pytest.main(['testcase/', '-s', '-v', '-q', '--alluredir', 'html'])
   #通过allure工具生成我们需要的美观的测试报告
   os.system('allure.bat generate html -o report --clean')

"""
"-V"输出详细信息
"-s"输出测试函数或者测试方法里面print()打印出的内容
"--clean"存在相同目录则先进行清除
"--alluredir","./report/result"在目录下生成json文件
"""