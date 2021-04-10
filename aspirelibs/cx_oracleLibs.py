#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2021-2-28
@author: cgs
'''
import cx_Oracle
import json
import os
import time

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class cxOracle(object):

    def __init__(self,connstr):
        self.connect = cx_Oracle.Connection(connstr)#pylint: disable=c-extension-no-member
        self.cursor = self.connect.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connect.close()
    
    def update (self,sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            print("update OK")
        except Exception as error:
            print("更新失败：{}".format(error))
        finally:
            self.disconnect()
    
    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            print("delete OK")       
        except Exception as error:
            print("删除失败：{}".format(error))
        finally:
            self.disconnect()

    def insert(self,sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            print("insert OK")
        except Exception as error:
            print("插入数据失败：{}".format(error))
        finally:
            self.disconnect()
    
    def insert_list_param(self,sql,list_param):
        try:
            self.cursor.executemany(sql,list_param)
            self.connect.commit()
            print("insert OK")
        except Exception as error:
            print("插入数据失败：{}".format(error))
        finally:
            self.disconnect()

    def Selectone(self,sql):
        try:
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            return rs[0][0]
        except Exception as error:
            print("查询失败：{}".format(error))
        finally:
            self.disconnect()

    def Selectall(self,sql):
        try:
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            print("select OK")
            return rs
        except Exception as error:
            print("查询失败：{}".format(error))
        finally:
            self.disconnect()

    def execute_file(self,file):
        try:
            f = open(file,"r",encoding='UTF-8')
            full_sql = f.read()
            sql_commands = full_sql.split(';')
            for sql_command in sql_commands:
                sql_command = sql_command.strip()
                if sql_command !='':
                    self.cursor.execute(sql_command)
                    self.connect.commit()
        except Exception as error:
            print("执行脚本文件失败：{}".format(error))
        finally:
            self.disconnect()

    #输出json
    def Select_one_json(self,sql):
        try:
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            cols = [d[0] for d in self.cursor.description]
            for row in rs:
                dictstr = dict(zip(cols,row))
            js = json.dumps(dictstr,ensure_ascii=False,separators=(',', ':'))
            return js
        except Exception as error:
            print("输出单个json数据失败：{}".format(error))
        finally:
            self.disconnect

    # 以list输出json
    def Select_list_json(self,sql):
        try:
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            clos = [d[0] for d in self.cursor.description]
            list = []
            for row in rs:
                b = dict(zip(clos,row))
                list = list + [b]
            #json.dumps序列化时对中文默认使用的ascii编码，输出真正的中文需要指定ensure_ascii=False    
            js = json.dumps(list,ensure_ascii=False, separators=(',', ':'))           
            return js
        except Exception as error:
            print("输出list的json错误：{}".format(error))
        finally:
            self.disconnect
                
if __name__ == '__main__':
    '''
    print("删除数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    db.delete("DELETE FROM BAC_CUSTOM_20210301TEST WHERE CUSTOMNAME LIKE '陈国森%'")    
    
    start =time.time()
    print("查询单个数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    print(db.Selectone("SELECT COUNT(*)  FROM BAC_AP_CONFIG_20210226test"))
    end = time.time()
    print('Running time: {:.2f} Seconds'.format(end-start))
    
    print("查询全部数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    print(db.Selectall("SELECT * FROM BAC_AP_CONFIG_20210226test"))
    
    print("插入数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    
    print("更新数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    db.update("UPDATE BAC_AP_CONFIG_20210226test SET SYSTEMCODE = 'ADVERT00' WHERE SYSTEMCODE = 'ADVERT33'")  
    
    print("更新LIST数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    param = [(2103069,'999','陈国森1','11'),(3103069,'888','陈国森2','22')]
    db.insert_list_param("insert INTO PDC.BAC_CUSTOM_20210301TEST (CUSTOMID,IDENTITYNUMBER,CUSTOMNAME,CUSTOMTYPE) VALUES (:1,:2,:3,:4)",param)
    
    print("执行脚本文件----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')     
    db.execute_file("D:\\app\\AspBac\\testdata\\init_OpenAccount.sql")
    '''
    print("输出单个jon数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    print(db.Select_one_json("SELECT acctStatus,TO_NUMBER(TO_DATE(createTime) - TO_DATE('1970-01-01 8:0:0', 'YYYY-MM-DD HH24:MI:SS')) * 86400000 AS createTime,customId,innerUserId,userEmail,userId,userMobile,userName,userSource,userType FROM BAC_USER WHERE USERID ='900002'").lower())
    '''
    print("输出list格式的json数据-----------------------------------------------------------------------------------")
    db = cxOracle('pdc/pdc456@10.12.3.240:1521/db240')
    print(db.Select_list_json("SELECT systemcode,systemcodename,SYSTEMCODELEVEL FROM BAC_AP_CONFIG_20210226test bac"))
    '''
