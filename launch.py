# coding=utf-8
import sys,os
from common import constants

sys.path.append(constants.TEST_DIR + "/libs")
from utils import log
from main.controller import Controller




def launch():
    args = sys.argv
    # check path and params
    if(not is_int(args) or not is_normal_path()):
        print(is_normal_path())
        log.fail_msg('Check path and params Fail,Please check!!!')
        return

    # !!! For gold sample test you can comment it
    # get hardware configuration from mes
    # if not hw_cfg.get_hw_cfg():
    #     log.fail_msg("get sample configure Fail!!!")
    #     sys.exit(1)

    c = Controller()
    # start all test
    if len(args) == 1:
        c.start_helper()
    # start station test
    elif len(args) == 2:
        c.start_helper(args[1]) 
    # start item test for debug
    else:
        c.start_helper(args[1],args[2])

# 判断是不是int类型
def is_int(v):
    if(type(v) == int):
        return True
    elif (type(v) == list):
        for item in v[1:]:
            try:
                int(item)
            except ValueError:
                return False
        return True
    return False

# 判断测试路径是否正确
def is_normal_path():
    return os.getcwd() == constants.TEST_DIR

if __name__ == '__main__':
   launch()