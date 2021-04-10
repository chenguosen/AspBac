#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2021-2-28
@author: cgs
'''

from jpype import *
import os.path

def DSA_sign(content, keyStr):
    # 这里传参，参数两个content, keyStr
    # 这里传参可以先写默认值，我这里的默认值都是''空，有默认值时robotframework调用时可以不传参
    # 也可以不要默认值，不哟啊默认值在调用时必须传参，不然会报错，
    # 不要默认值上面该这样写：getliveparam(content, keyStr)
    """
    传入两个值content、keyStr并返回加密值base64param

    查看注释
    Example:
    | ${result}        | getliveparam          | content         | keyStr    |
    """
    # 获取jar包地址，os.path.abspath('.')返回当前工作地址，也就是robotframework项目文件夹
    home = os.path.abspath('.')
    jarpath = os.path.join(os.path.abspath('.'), home + '\javalibs\sign.jar')
    print("jar包的路径是：{}".format(jarpath))
    # 上面那句也可以如下写成绝对地址，写成绝对地址时可以将jar包放在任意位置，但jar位置变了这里就得改
    #jarpath = os.path.join(os.path.abspath('.'), 'D:/test/javalibs/Execute02.jar')

    # 启动java虚拟机
    if not isJVMStarted():  # 如果jvm没启动才执行启动操作
        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)

    # 获取类，这里是包名和类名，报名从第一层开始写
    Execut = JClass('sign.util.SignUtil')
    # 或者通过JPackage引用Test类
    # com = JPackage('test.authentication').Execute02()

    # 调用相关方法函数
    t = Execut()
    #res = t.encryptBy3DesAndBase64(content, keyStr)
    res = t.buildSign(keyStr, content)
    print(content)

    # 返回从java方法中获取的值
    return res
    shutdownJVM()


# 用完后记得关闭java虚拟机，当然python程序退出时JVM也会自动关闭
if __name__ == '__main__':
    home = os.path.abspath('.')
    print(home)
    sign_str = '''{"pubInfo":{"systemCode":"ASPTEST2","msgVer":"1.0","reqTime":"20210317085955"},"openAcctInfo":{"userInfo":{"bindMobile":"15818640854","userId":"900004","email":"qiuhaiyang@139.com"},"normalAcctPayType":1,"contractInfo":{"contractId":"9000000000000200004"},"contractAcctPayType":1,"acctType":"10","validTime":"","customInfo":{"identityNumber":"100000004","customName":"OCE"},"invalidTime":"","busiTypeList":"13","creditWoffResume":1,"acctName":"陈国森4"}}'''
    pem_private_key = "MIIBSwIBADCCASwGByqGSM44BAEwggEfAoGBAP1/U4EddRIpUt9KnC7s5Of2EbdSPO9EAMMeP4C2USZpRV1AIlH7WT2NWPq/xfW6MPbLm1Vs14E7gB00b/JmYLdrmVClpJ+f6AR7ECLCT7up1/63xhv4O1fnxqimFQ8E+4P208UewwI1VBNaFpEy9nXzrith1yrv8iIDGZ3RSAHHAhUAl2BQjxUjC8yykrmCouuEC/BYHPUCgYEA9+GghdabPd7LvKtcNrhXuXmUr7v6OuqC+VdMCz0HgmdRWVeOutRZT+ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN/C/ohNWLx+2J6ASQ7zKTxvqhRkImog9/hWuWfBpKLZl6Ae1UlZAFMO/7PSSoEFgIURsjR4M8E+qPp2jPd46ZmRx3gqd8="
    res = DSA_sign(sign_str, pem_private_key)
    print(res)
    print()