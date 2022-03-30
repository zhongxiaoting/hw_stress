# coding=utf-8
import os
import re
import sys
import time

from main.item import Item
from utils import decorator
from common import common_value as cv, constants as c

sys.path.append("..")
# CPU MCE检测
CMD_GET_CPU_MCE = 'ras-mc-ctl --summary'


class MCE_ECC(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.cpu_mce_check()
        self.mem_ecc_check()

    # CPU MCE检测
    @decorator.item_test
    def cpu_mce_check(self):
        # 安装CPU MEC检测工具
        # aa = self.run_cmd("cd tools && sh rasdaemon.sh")
        cpu_mec_display = self.run_cmd(CMD_GET_CPU_MCE)
        write_log("=============  CPU MCE Check Begin  " + get_local_time_string() + " ================")
        write_log(cpu_mec_display)
        write_log("==============  CPU MCE Check End  " + get_local_time_string() + " =================")
        self.cpu_mce_errors(cpu_mec_display)
        return cpu_mec_display

    # 内存ECC检测
    def mem_ecc_check(self):
        ecc_clear = self.run_cmd("ipmitool sel clear")
        ecc_infor = self.run_cmd("ipmitool sel list")
        write_log("=============  MEM ECC Check Begin  " + get_local_time_string() + " ================")
        write_log(ecc_infor)
        write_log("==============  MEM ECC Check End  " + get_local_time_string() + " =================")
        if "ECC" in ecc_infor:
            write_log("->>>\033[31m MEM ECC Fail \033[0m")
            self.result_fail()
            return
        write_log("->>>\033[32m MEM ECC PASS \033[0m")
        return


    # CPU MCE 检测出现错误
    def cpu_mce_errors(self, mce_errors):
        temp = mce_errors.split('\n')
        for mce in temp:
            if mce == '':
                continue
            result = re.match("No", mce)
            if not result:
                errors_information = self.run_cmd("ras-mc-ctl --errors")
                write_log("============  CPU MCE ERROR Check Begin " + get_local_time_string() + " ==============")
                write_log(errors_information)
                write_log("==============  CPU MCE ERROR Check End " + get_local_time_string() + " ================")
                write_log("->>>\033[31m MCE ERROR \033[0m")
                self.result_fail()
                return errors_information
            else:
                write_log("->>>\033[32m  CPU MCE PASS \033[0m")
            return


def write_log(s):
    with open(c.MCE_ECC_LOG, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))