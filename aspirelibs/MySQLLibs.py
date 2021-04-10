'''
Created on 2020年5月19日

@author: xiecs
'''

import pymysql
        
class MySQLHelper(object):
    '''
    classdocs
    '''
    __conn = None
    __cursor = None
    conn_params = None
    def __init__(self, connstr):
        '''
        Constructor
        '''
        params = connstr.split(',')
        self.conn_params = {}
        for i in params:
            kv = i.split('=')
            self.conn_params[kv[0]] = kv[1]
        self.conn_params['port'] = int(self.conn_params.get('port'))
     
    def get_conn(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                host=self.conn_params.get('host'),
                user=self.conn_params.get('user'),
                passwd=self.conn_params.get('passwd'),
                db=self.conn_params.get('db'),
                port=self.conn_params.get('port'),
                charset=self.conn_params.get('charset')) 
            self.__cursor = self.__conn.cursor()

    def get_conn_dic(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                host=self.conn_params.get('host'),
                user=self.conn_params.get('user'),
                passwd=self.conn_params.get('passwd'),
                db=self.conn_params.get('db'),
                port=self.conn_params.get('port'),
                charset=self.conn_params.get('charset')) 
            self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
          
    def close(self):
        if self.__cursor is not None:
            self.__cursor.close()
            
        if self.__conn is not None:
            self.__conn.close()
            
    def execute(self, sql, param=None, autoclose=False):
        count = 0
        self.get_conn()
        try:
            if param:
                count = self.__cursor.execute(sql, param)
            else:
                count = self.__cursor.execute(sql)
                
            self.__conn.commit()

            if autoclose:
                self.close()
        except Exception as e:
            print("error_msg:", e.args)
        
        return count

    def execute_dic(self, sql, param=None, autoclose=False):
        count = 0
        self.get_conn_dic()
        try:
            if param:
                count = self.__cursor.execute(sql, param)
            else:
                count = self.__cursor.execute(sql)
                
            self.__conn.commit()

            if autoclose:
                self.close()
        except Exception as e:
            print("error_msg:", e.args)
        
        return count
    
    def selectone(self, sql, param=None):
        try:
            count = self.execute(sql, param)
            res = self.__cursor.fetchone()
            self.close()
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close()
            return count
        
    def select(self, sql, param=None):
        try:
            count = self.execute(sql, param)
            res = self.__cursor.fetchall()
            self.close()
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close()
            return count
    
    def insertone(self, sql, param):
        try:
            count = self.execute(sql, param)
            self.__conn.commit()
            self.close()
            return count
        except Exception as e:
            print(e)
            self.__conn.rollback()
            self.close()
            return count
        
    def delete(self, sql, param=None):
        try:
            count = self.execute(sql, param)
            self.close()
            return count
        except Exception as e:
            print(e)
            self.__conn.rollback()
            self.close()
            return count
        
    def update(self, sql, param=None):
        try:
            count = self.execute(sql, param)
            self.__conn.commit()
            self.close()
            return count
        except Exception as e:
            print(e)
            self.__conn.rollback()
            self.close()
            return count

    #查询结果以字典格式输出
    def select_dic(self, sql):
        try:
            # 使用 execute_dic() 执行sql
            count = self.execute_dic(sql)
            # 使用 fetchall() 获取查询结果
            res = self.__cursor.fetchall()
            self.close()
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close()
            return count

def main():
        print("test db")
        db = MySQLHelper("host=10.12.3.235,port=3306,user=tstfabric1,passwd=tstfabric1,db=db_tstfabric1,charset=utf8")

        rec = db.select("SELECT  * FROM t_transaction WHERE tid = '10010258-20200410132322-29998068';")
        print(rec)
    
if __name__ == '__main__':
    main()

        
        
