import configparser
import os
#import os.path

default_config_name = 'config.ini'

def get_sections():
    '''
        返回节点列表
    '''
    cf = configparser.RawConfigParser()
    cf.read(os.path.abspath(default_config_name))
    return cf.sections()
    
def get_options(section_name):
    '''
        返回给定节点的键列表
    '''
    cf = configparser.RawConfigParser()
    cf.read(os.path.abspath(default_config_name))
    return cf.options(section_name) 

def get_items(section_name):
    '''
        返回给定节点的值列表
    '''
    cf = configparser.RawConfigParser()
    cf.read(os.path.abspath(default_config_name))
    return cf.items(section_name) 

def get_value(section_name, key_name):
    '''
        返回给定节点的某个值列表
    '''
    cf = configparser.RawConfigParser()
    cf.read(os.path.abspath(default_config_name))
    return cf.get(section_name, key_name) 


if __name__ == '__main__':
    print(get_value("Common","ServAddr"))
    print(get_value("Common","db_conn"))
    print(get_value("Common","privatekey2"))

    home = os.path.abspath('.')
    print(home)

