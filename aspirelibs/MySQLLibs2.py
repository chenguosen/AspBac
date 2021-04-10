'''
Created on 2020年5月19日

@author: xiecs
'''

import pymysql
from dbutils.pooled_db import PooledDB

class PooledMySQL(object):
    __pool = None
    __conn_params = {}
    def __init__(self, connstr):
        params = connstr.split(',')
        for i in params:
            kv = i.split('=')
            self.__conn_params[kv[0]] = kv[1]
        self.__conn_params['port']=int(self.__conn_params.get('port'))

        self.getconn()
        
    def __enter__(self):
        self.conn = self.__getconn()
    
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=pymysql,
                mincached=0,
                maxcached=3,
                maxshared=5,
                maxconnections=5,
                blocking=True,
                maxusage=0,
                setsession=None,
                host=self.__conn_params.get('host'),
                port=self.__conn_params.get('port'),
                user=self.__conn_params.get('user'),
                passwd=self.__conn_params.get('passwd'),
                db=self.__conn_params.get('db'),
                charset=self.__conn_params.get('charset')
                )
        
        return self.__pool.connection()
    
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn
    
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.cursor.close()
#         self.conn.close()
        
class MySQLHelper(object):
    '''
    classdocs
    '''

#     __conn = None
#     __cursor = None
    
    def __init__(self, connstr):
        '''
        Constructor
        '''
        self.db = PooledMySQL(connstr)
        
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, 'inst'):  # 单例
#             cls.inst = super(MySQLHelper, cls).__new__(cls, *args, **kwargs)
#         return cls.inst
#            
    def close(self, cursor, conn):
        if cursor is not None:
            conn.close()
            
        if conn is not None:
            conn.close()
            
    def execute(self, sql, param=None, autoclose=False):
        cursor, conn = self.db.getconn()
        count = 0
        
        try:
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
                
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            print("error_msg:", e.args)
        
        return cursor, conn, count
    
    def selectone(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close(cursor, conn)
            return count
        
    def select(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchall()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close(cursor, conn)
            return count
    
    def insertone(self, sql, param):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count
        
    def insertmany(self, sql, param):
        '''
        :param sql:
        :param param: 必须是元组或列表[(),()]或（（），（））
        :return:
        '''
        cursor, conn, count = self.db.getconn()
        try:
            cursor.executemany(sql, param)
            conn.commit()
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count
        
    def delete(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count
        
    def update(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

def main():
        print("test db")
        db=MySQLHelper("host=10.12.3.235,port=3306,user=tstfabric1,passwd=tstfabric1,db=db_tstfabric1,charset=utf8")

        rec = db.select("SELECT  * FROM t_transaction WHERE tid = '10010258-20200410132322-29998068';")
        print(rec)
    
if __name__ == '__main__':
    main()

        
        