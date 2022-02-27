# coding=utf-8
import os
import time

from main.item import Item
import sys
from common import common_value as cv, constants as c

sys.path.append("..")


class MEM_STRESS(Item):
    def __init__(self, info):
        super(MEM_STRESS, self).__init__()
        self.info = info

    def run_item(self):
        self.mem_check()

    def get_mem(self):
        out = self.run_cmd("free -m|grep Mem")
        mem = out.split()[3]
        print(mem)
        return int(mem) - 10240

    def mem_check(self):
        cv.remove_log(c.MEM_STRESS_LOG_PATH)
        free_mem = 10240
        # free_mem = self.get_mem() * 0.98
        write_log("=============  MEM Stress Check Begin  " + get_local_time_string() + " ================")
        shell = "timeout {} memtester {} 1 >> {}".format(c.RUN_SECONDS, int(free_mem), c.MEM_STRESS_LOG_PATH)
        write_log("The Command Line ->>> " + shell + "\n")
        mem_infor = self.run_cmd(shell)
        write_log("\n" + "==============  MEM Stress Check End  " + get_local_time_string() + " =================")
        return mem_infor


def write_log(s):
    with open(c.MEM_STRESS_LOG_PATH, 'a+') as f:
        # print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))
