#coding utf-8
'''
@author: xiecs
'''

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

def kafkaSendMsg(btServers, topic, message):
    try:
        kafkaMgr.producer = KafkaProducer(bootstrap_servers=btServers) 
    except Exception as e:
        print("kafka producer connection failed")
        print(e);
    
    try:
        kafkaMgr.producer.send(topic, message)
        kafkaMgr.producer.flush(20)
        kafkaMgr.producer.close(20)
        kafkaMgr.producer = None
    except KafkaError as e:
        print("kafka send failed")
        print(e)
    
def kafkaStartToRecv(btServers, topicid, groupid,timeout_ms=10000):
    try:
        kafkaMgr.consumer = KafkaConsumer(topicid, group_id = groupid, bootstrap_servers=btServers, consumer_timeout_ms=int(timeout_ms))
    except Exception as e:
        print("kafka consumer connect failed")
        print(e)
            
    except KafkaError:
        print("kafka receive message failed")

def _ConsumeData():
    print("Start to receive data")
    if kafkaMgr.consumer == None:
        print("consumer is None!")
        return
    for receiveMsg in kafkaMgr.consumer:
        yield receiveMsg

def kafkaConsumeData(message_key=None):
    messages = _ConsumeData()
    for m in messages:
        kafkaMgr.lastMsg = m.value
        if message_key != None:
            if message_key in m.value:
                break

def getLastMessage():
    return kafkaMgr.lastMsg

def kafkaClose():
    try:
        if kafkaMgr.consumer!=None:
            kafkaMgr.consumer.close()
            kafkaMgr.consumer = None
        if kafkaMgr.producer!=None:
            kafkaMgr.producer.close()
            kafkaMgr.producer = None
        
        if kafkaMgr.lastMsg!=None:
            kafkaMgr.lastMsg=None
            
    except Exception:
        print('err')    
            
class kafkaMgr():
    producer = None
    consumer = None
    lastMsg = None