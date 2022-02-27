# coding=utf-8
import os
import sys
import time

from main.item import Item
from utils import decorator
from common import common_value as cv, constants as c

sys.path.append("..")


class CPU_STRESS(Item):
    def __init__(self, info):
        super(CPU_STRESS, self).__init__()
        self.info = info

    def run_item(self):
        self.stress_check()

    def getCurrentcpuuse(self):
        out = self.run_cmd("cat /proc/stat|head -n 1")
        l = out.split()
        user = int(l[1])
        nice = int(l[2])
        sys = int(l[3])
        idle = int(l[4])
        currentcpuuse = (user + sys) / (user + nice + sys + idle)
        return currentcpuuse

    def get_thread_num(self):
        core_num = self.run_cmd("cat /proc/cpuinfo | grep -c processor")
        freecpu = 1 - self.getCurrentcpuuse()
        threadnum = int(freecpu * (int(core_num) - 1))
        return threadnum

    def stress_check(self):
        threadnum = self.get_thread_num()
        cv.remove_log(c.CPU_STRESS_LOG_PATH)
        shell = "stress -c {} -t {} ".format(threadnum, c.RUN_SECONDS)
        # print(cpu_infor)
        write_log("=============  CPU Stress Check Begin  " + get_local_time_string() + " ================")
        write_log("The Command Line ->>> " + shell + "\n")
        cpu_infor = self.run_cmd(shell)
        write_log(cpu_infor)
        write_log("==============  CPU Stress Check End  " + get_local_time_string() + " =================")
        return cpu_infor


def write_log(s):
    with open(c.CPU_STRESS_LOG_PATH, 'a+') as f:
        # print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))
