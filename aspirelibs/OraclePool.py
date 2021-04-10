# -*- coding: utf-8 -*-
 
"""
--------------------------------------
@File       : oracle_pool.py
@Author     : cgs
@Created on : 2021/3/15 15:47
--------------------------------------
"""
 
import cx_Oracle as Oracle
from dbutils.pooled_db import PooledDB
import time
 
 
class OraclePool:
    """
    1) 这里封装了一些有关oracle连接池的功能;
    2) sid和service_name，程序会自动判断哪个有值，
        若两个都有值，则默认使用service_name；
    3) 关于config的设置，注意只有 port 的值的类型是 int，以下是config样例:
        config = {
            'user':         'maixiaochai',
            'password':     'maixiaochai',
            'host':         '192.168.158.1',
            'port':         1521,
            'sid':          'maixiaochai',
            'service_name': 'maixiaochai'
        }
    """
 
    def __init__(self, config):
        """
        获得连接池
        :param config:      dict    Oracle连接信息
        """
        self.__pool = self.__get_pool(config)
 
    @staticmethod
    def __get_pool(config):
        """
        :param config:        dict    连接Oracle的信息
        ---------------------------------------------
        以下设置，根据需要进行配置
        maxconnections=6,   # 最大连接数，0或None表示不限制连接数
        mincached=2,        # 初始化时，连接池中至少创建的空闲连接。0表示不创建
        maxcached=5,        # 连接池中最多允许的空闲连接数，很久没有用户访问，连接池释放了一个，由6个变为5个，
                            # 又过了很久，不再释放，因为该项设置的数量为5
        maxshared=0,        # 在多个线程中，最多共享的连接数，Python中无用，会最终设置为0
        blocking=True,      # 没有闲置连接的时候是否等待， True，等待，阻塞住；False，不等待，抛出异常。
        maxusage=None,      # 一个连接最多被使用的次数，None表示无限制
        setession=[],       # 会话之前所执行的命令, 如["set charset ...", "set datestyle ..."]
        ping=0,             # 0  永远不ping
                            # 1，默认值，用到连接时先ping一下服务器
                            # 2, 当cursor被创建时ping
                            # 4, 当SQL语句被执行时ping
                            # 7, 总是先ping
        """
        dsn = None
        host, port = config.get('host'), config.get('port')
 
        if 'service_name' in config:
            dsn = Oracle.makedsn(host, port, service_name=config.get('service_name'))#pylint: disable=c-extension-no-member
 
        elif 'sid' in config:
            dsn = Oracle.makedsn(host, port, sid=config.get('sid'))#pylint: disable=c-extension-no-member
 
        pool = PooledDB(
            Oracle,
            mincached=5,
            maxcached=10,
            user=config.get('user'),
            password=config.get('password'),
            dsn=dsn
        )
 
        return pool
 
    def __get_conn(self):
        """
        从连接池中获取一个连接，并获取游标。
        :return: conn, cursor
        """
        conn = self.__pool.connection()
        cursor = conn.cursor()
 
        return conn, cursor
 
    @staticmethod
    def __reset_conn(conn, cursor):
        """
        把连接放回连接池。
        :return: 
        """
        cursor.close()
        conn.close()
 
    def __execute(self, sql, args=None):
        """
        执行sql语句
        :param sql:     str     sql语句
        :param args:    list    sql语句参数列表
        :param return:  cursor
        """
        conn, cursor = self.__get_conn()
        
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
 
        return conn, cursor
 
    def fetch_all(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        result = cursor.fetchall()
        self.__reset_conn(conn, cursor)
 
        return result
 
    def fetch_one(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        result = cursor.fetchone()
        self.__reset_conn(conn, cursor)
 
        return result
 
    def execute_sql(self, sql, args=None):
        """
        执行SQL语句。
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        conn, cursor = self.__execute(sql, args)
        conn.commit()
        self.__reset_conn(conn, cursor)
 
    def __del__(self):
        """
        关闭连接池。
        """
        self.__pool.close()
 
 
if __name__ == "__main__":
    #demo()
    start =time.time()
    config = {
        'user': 'pdc',
        'password': 'pdc456',
        'host': '10.12.3.240',
        'port': 1521,
        'sid': 'PDC',
        'service_name': 'db240'
    }
 
    sql = "SELECT COUNT(*)  FROM BAC_AP_CONFIG_20210226test"
 
    orcl = OraclePool(config)
    result = orcl.fetch_one(sql)
    end = time.time()
    print(result)
    print('Running time: {:.2f} Seconds'.format(end-start))
    print("chenguosen")