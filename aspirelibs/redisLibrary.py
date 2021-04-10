# -*- coding: utf-8 -*-

'''
-------------------------------------------------
Created on 2017-7-10
@author: wangmianjie
install:
 easy_install redis
-------------------------------------------------
Change Activity:  cgs  2021/03/18
增加链接串的初始化处理
-------------------------------------------------
'''
import redis
from rediscluster import RedisCluster
from rediscluster import StrictRedisCluster


class redisHelper(object):

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

    def getRedisConn(self):

        hostIp = self.conn_params.get('hostIp')
        port = self.conn_params.get('port')
        isCluster = self.conn_params.get('isCluster')
        passwd = self.conn_params.get('passwd')

        if isCluster == '1':
            startup_nodes = [{"host": hostIp, "port": port}]
            return StrictRedisCluster(startup_nodes=startup_nodes, password=passwd, decode_responses=True)
        else:
            if(passwd is None):
                return redis.StrictRedis(hostIp, int(port))
            else:
                return redis.StrictRedis(hostIp, int(port), password=passwd)

    def redisFlushall(self,connstr):
        '''清空整个redis'''
        redisConn = self.getRedisConn()
        redisConn.flushall()

    ''' String类型操作'''

    def setString(self, key, value):
        """设置String类型的值
        """
        redisConn = self.getRedisConn()
        redisConn.set(key, value)

    def setStringForDict(self, redisDict):
        """批量设置String类型的 key和value，参数为dict类型
        """
        if type(redisDict) == "string":
            dictObj = eval(redisDict)
            redisConn = self.getRedisConn()
            for (key, value) in dictObj.items():
                redisConn.set(key, value)
        else:
            redisConn = self.getRedisConn()
            for (key, value) in redisDict.items():
                redisConn.set(key, value)
            

    def getStringByKey(self, key):
        """根据key获取值
        """
        redisConn = self.getRedisConn()
        return redisConn.get(key)

    ''' 集合操作 '''

    def saddOne(self, key, value):
        """设置一条集合类型的值
        """
        redisConn = self.getRedisConn()
        redisConn.sadd(key, value)

    def zaddOne(self, key, score, value):
        """设置一条有序集合类型的值
        """
        redisConn = self.getRedisConn()
        redisConn.zadd(key, score, value)

    def saddBatch(self, key, values):
        """向一个集合写入多个值， 值的格式为: a|b|c
        """
        redisConn = self.getRedisConn()
        valueList = values.split('|')
        for value in valueList:
            redisConn.sadd(key, value)

    def sremOne(self, key, value):
        """删除一条集合类型的值
        """
        redisConn = self.getRedisConn()
        redisConn.srem(key, value)

    def sremBatch(self, key, values):
        """删除一条集合类型的多个值,， 值的格式为: a|b|c
        """
        redisConn = self.getRedisConn()
        for value in values.split('|'):
            redisConn.srem(key, value)

    def sismember(self, key, value):
        """查看集合的一个值是否存在
        """
        redisConn = self.getRedisConn()
        return redisConn.sismember(key, value)

    ''' hash操作 '''

    def hset(self, name, key, value):
        """设置hash类型的的值，一次一条
        """
        redisConn = self.getRedisConn()
        redisConn.hset(name, key, value)

    def hsetByDict(self, name, dict):
        """向集合类型的key批量增加值，
        """
        dictObj = eval(dict)
        redisConn = self.getRedisConn()
        for (key, value) in dictObj.items():
            redisConn.hset(name, key, value)

    def hget(self, name, key):
        """取一个hash的某个key的值
        """
        redisConn = self.getRedisConn()
        return redisConn.hget(name, key)

    def hdel(self, name, key):
        """删除hash类型数据的一个字段
        """
        redisConn = self.getRedisConn()
        redisConn.hdel(name, key)

    def getVerifyCode(self, key):
        """
        获取value，string类型，value以：分隔
        """
        redisConn = self.getRedisConn()
        return redisConn.get(key).split(':')[1]

    def getVerifyCodeIVR(self, key):
        """
        获取value，string类型，value以：分隔
        """
        redisConn = self.getRedisConn()
        return redisConn.get(key).split(',')[1]

    def getVerifyCodePicSms(self,VerifyCode):
        smsVerifyCode = VerifyCode.split(';')[0].split(':')[1]
        pictureVerifyCode = VerifyCode.split(';')[1].split(':')[1]
        return smsVerifyCode, pictureVerifyCode

    def delete(self, key):
        """删除key
        """
        redisConn = self.getRedisConn()
        redisConn.delete(key)

    def deleteList(self, keys):
        """批量删除key,参数为List
        """
        redisConn = self.getRedisConn()
        for key in keys:
            redisConn.delete(key)       

    def getFieldValueByHash(self, key, fieldName):
        redisConn = self.getRedisConn()
        dict = redisConn.hgetall(key)
        return dict[fieldName]
    '''
    def delFieldByHash(self,hostIp, port, isCluster, passwd, key, fieldName):
        edisConn = self.getRedisConn(hostIp, port, isCluster, passwd)
        redisConn.hdel(key, fieldName)
    '''


if __name__ == "__main__":

    #单实例
    #redis_conn = "hostIp=10.12.3.134,port=6380,isCluster=0,passwd=test123"
    redis_conn = "hostIp=10.1.5.150,port=8001,isCluster=1,passwd="
    keys = ['BAC_account_userId_900002', 'BAC_user_userId_900002',
            'BAC_BASR_16_9000000000000200004', 'BAC_custom_idEntityNumber_100000002']
    for key in keys:
        red = redisHelper(redis_conn)
        #red.delete(key)
        print(red.getStringByKey(key))
    '''
    value = '{"acctSubjectIdBase":113210025,"acctSubjectIdGive":213210025,"busiType":"13","contractId":"91000000000000010005"}'
    key ='BAC_BASR_16_91000000000000010005'
    red = redisHelper(redis_conn)
    #red.setString(key,value)
    print(red.getStringByKey(key))
    '''






