'''
Created on 2020年5月26日

@author: xiecs
'''
import re
import random
import uuid
import json
from aspirelibs.JSONLibrary import JSONObject

def match_test_rule_value(src):
    '''
       通过执行命令，替换掉某些符合特定规律的数据
       返回List对象
    uuid1()基于MAC地址，时间戳，随机数来生成唯一的uuid，可以保证全球范围内的唯一性
    uuid2()算法与uuid1相同，不同的是把时间戳的前4位置换为POSIX的UID
    uuid3~uuid5存在一定的相同概率
    '''
    # []表示需要执行其中的命令
    pattern = r'\[(.+?)\]'
    result = re.findall(pattern, src)
    for rs in result:
        exec_r1 = eval(rs)
        pattern = r'(\[.+?\])'
        src = re.sub(pattern, str(exec_r1), src, 1)
    
    kvs = src.split('|')
    return kvs    
    
def match_node_rule_value(json_obj):
    json_str=json.dumps(json_obj)
    pattern = r'\<(.+?)\>'
    result = re.findall(pattern, json_str)
    for rs in result:
        val = JSONObject.get_value_from_json(None, json_obj, rs)
        pattern = r'(\<.+?\>)'
        json_str = re.sub(pattern, str(val[0]), json_str, 1)
        json_obj = json.loads(json_str)
    return json_obj
    
def main():
    src = 'aaadfdsafasfd[random.randint(5,10)]adfadsf[uuid.uuid1()]adsfsaf'
    print(match_test_rule_value(src))
    
if __name__ == '__main__':
    main()