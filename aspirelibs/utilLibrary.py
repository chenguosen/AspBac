# coding:utf-8
import socket
import random
import string

def compare_list(rList, eList):
    if (type(rList) != type (eList)):
        return False

    if((rList == None) & (eList == None)):
        return u'True'
     
    if(len(rList) != len(eList)):
        return False
    
    for i in range(len(rList)):
        if rList[i] not in eList:
            return False

    for i in range(len(eList)):
        if eList[i] not in rList:
            return False
    
    return True

def contain_list(rList, eList):
    if (type(rList) != type (eList)):
        return False

    if((rList == None) & (eList == None)):
        return True
        
    for i in range(len(eList)):
        if eList[i] not in rList:
            return False
    
    return True

def get_var_length(info):
    '''
    ' 获取数据库查询结果的长度，类型不同
    '''
    if (isinstance(info, None)):
        return 0
    elif (isinstance(info, tuple)):
        return 1
    elif (isinstance(info, list)):
        return len(info)
    
def result_to_list_ex(keys, data):
    '''
    # 将数据库数据转换成List格式
    '''
    # 无数据，返回结果需要看具体需求而定，可能返回None，可能返回[]
    if (isinstance(data, None)):
        return None
    # 仅有一条记录，查询 结果是元组
    elif(isinstance(data, tuple)):
        if(len(keys) != len(data)):
            return None
        rList = []
        dic = {}
        for i in range(len(keys)):
            if(keys[i].lower().startswith('(int)')):
                key = keys[i].lstrip('(int)')
                value = int(data[i])
            elif(keys[i].lower().startswith('(float)')):
                key = keys[i].lstrip('(float)')
                value = float(data[i])
            else:
                key = keys[i]
                value = data[i]
            dic[key] = value
        rList.append(dic)
        return rList
    # 存在多条数据，查询结果是List
    elif(isinstance(data, list)):
        if(len(keys) != len(data[0])):
            return None        
        iLen = len(data)  # 记录行数
        jLen = len(data[0])  # 记录字段数
        
        rList = []
        for i in range(iLen):
            dic = {}
            for j in range(jLen):
                if(keys[j].lower().startswith('(int)')):
                    key = keys[j].lstrip('(int)')
                    value = int(data[i][j])
                elif(keys[j].lower().startswith('(float)')):
                    key = keys[j].lstrip('(float)')
                    value = float(data[i][j])
                else:
                    key = keys[j]
                    value = data[i][j]
                dic[key] = value
            
            rList.append(dic)
            
        return rList
    
def result_append_list(sList, keys, data):
    '''
    # 将数据库数据转换成List格式
    '''

    # 无数据，返回结果需要看具体需求而定，可能返回None，可能返回[]
    if (isinstance(data, None)):
        return sList
    # 仅有一条记录，查询 结果是元组
    elif(isinstance(data, tuple)):
        if(len(keys) != len(data)):
            return sList
            # 无数据，返回结果需要看具体需求而定，可能返回None，可能返回[]
        if (isinstance(data, list)):
            sList = []
        dic = {}
        for i in range(len(keys)):
            if(keys[i].lower().startswith('(int)')):
                key = keys[i].lstrip('(int)')
                value = int(data[i])
            elif(keys[i].lower().startswith('(float)')):
                key = keys[i].lstrip('(float)')
                value = float(data[i])
            else:
                key = keys[i]
                value = data[i]
            dic[key] = value
        sList.append(dic)
        return sList
    # 存在多条数据，查询结果是List
    elif(isinstance(data, list)):
        if(len(keys) != len(data[0])):
            return sList
        if (isinstance(data, None)):
            sList = []      
        iLen = len(data)  # 记录行数
        jLen = len(data[0])  # 记录字段数
        
        for i in range(iLen):
            dic = {}
            for j in range(jLen):
                if(keys[j].lower().startswith('(int)')):
                    key = keys[j].lstrip('(int)')
                    value = int(data[i][j])
                elif(keys[j].lower().startswith('(float)')):
                    key = keys[j].lstrip('(float)')
                    value = float(data[i][j])
                else:
                    key = keys[j]
                    value = data[i][j]
                dic[key] = value
            
            sList.append(dic)
            
        return sList
    
def tuple_to_list(data):
    '''
    # 将数据库数据转换成List格式
    '''
    # 无数据，返回结果需要看具体需求而定，可能返回None，可能返回[]
    if (isinstance(data, None)):
        return []
    # 仅有一条记录，查询 结果是元组
    elif(isinstance(data, tuple)):
        rList = []
        for i in range(len(data)):
            rList.append(data[i])
        return rList
    # 存在多条数据，查询结果是List
    elif(isinstance(data, list)):
        rList = []
        for i in range(len(data)):
            if(isinstance(data, tuple)):
                rList.append(data[i][0])
            else:
                rList.append(data[i])
            
        return rList
    
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    print(ip)
    return ip    
            
def create_random_string(lbound, rbound, opertype=0):
    str = ''
    lbound=int(lbound)
    rbound=int(rbound)
    opertype=int(opertype)
    if opertype == 0:
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            chartype = random.randint(0, 5)
            if ((chartype == 0) and ((i + 2) < len)) :  # 汉字
                head = random.randint(0xb0, 0xf7)
                body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
                val = f'{head:x}{body:x}'
                str += bytes.fromhex(val).decode('gb2312')
                i += 2
            elif chartype == 1: #大小写字母
                s = string.ascii_letters
                str += random.choice(s)
                i += 1
            elif chartype == 2: #小写字母
                s=string.ascii_lowercase
                str += random.choice(s)
                i += 1
            elif chartype == 3: #大写字母
                s=string.ascii_uppercase
                str += random.choice(s)
                i += 1
            elif chartype == 4: #特殊字符
                str += random.choice('!@#$%^&*()')
                i += 1
            else:  # 数字
                s = string.digits
                str += random.choice(s)
                i += 1
    elif opertype == 1: #大小写
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            s = string.ascii_letters
            str += random.choice(s)
            i += 1
    elif opertype == 2: #小写
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            s = string.ascii_lowercase
            str += random.choice(s)
            i += 1
    elif opertype == 3: #大写
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            s = string.ascii_uppercase
            str += random.choice(s)
            i += 1
    elif opertype == 4: #特殊字符
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            chartype=random.randint(0,2)
            if chartype == 0:
                s = string.ascii_letters
            elif chartype==1:
                s= string.digits
            else:
                s='!@#$%^&*()'
            str += random.choice(s)
            i += 1        
    elif opertype == 5: #汉字
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            str += bytes.fromhex(val).decode('gb2312')
            i += 2
    else:
        len = random.randint(lbound, rbound)
        i = 0
        while i < len:
            s = string.digits
            str += random.choice(s)
            i += 1
                
    return str

def create_fixed_string(str_len, opertype=0):
    str = ''
    opertype=int(opertype)
    if opertype == 0:
        i = 0
        while i < str_len:
            chartype = random.randint(0, 5)
            if ((chartype == 0) and ((i + 2) < len)) :  # 汉字
                head = random.randint(0xb0, 0xf7)
                body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
                val = f'{head:x}{body:x}'
                str += bytes.fromhex(val).decode('gb2312')
                i += 2
            elif chartype == 1: #大小写字母
                s = string.ascii_letters
                str += random.choice(s)
                i += 1
            elif chartype == 2: #小写字母
                s=string.ascii_lowercase
                str += random.choice(s)
                i += 1
            elif chartype == 3: #大写字母
                s=string.ascii_uppercase
                str += random.choice(s)
                i += 1
            elif chartype == 4: #特殊字符
                str += random.choice('!@#$%^&*()')
                i += 1
            else:  # 数字
                s = string.digits
                str += random.choice(s)
                i += 1
    elif opertype == 1: #大小写
        i = 0
        while i < str_len:
            s = string.ascii_letters
            str += random.choice(s)
            i += 1
    elif opertype == 2: #小写
        i = 0
        while i < str_len:
            s = string.ascii_lowercase
            str += random.choice(s)
            i += 1
    elif opertype == 3: #大写
        i = 0
        while i < str_len:
            s = string.ascii_uppercase
            str += random.choice(s)
            i += 1
    elif opertype == 4: #特殊字符
        i = 0
        while i < str_len:
            chartype=random.randint(0,2)
            if chartype == 0:
                s = string.ascii_letters
            elif chartype==1:
                s= string.digits
            else:
                s='!@#$%^&*()'
            str += random.choice(s)
            i += 1        
    elif opertype == 5: #汉字
        i = 0
        while i < str_len:
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            str += bytes.fromhex(val).decode('gb2312')
            i += 2
    else:
        i = 0
        while i < str_len:
            s = string.digits
            str += random.choice(s)
            i += 1
                
    return str