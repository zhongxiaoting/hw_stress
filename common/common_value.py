# coding=utf-8
from utils import log as l, handle as h
from main.item import Item
import os
import commands


def get_cpu_information(cpu_infor):
    cpu = []
    for temp in cpu_infor:
        cpu_first = temp[0]
        # print(temp)
        l.log(cpu_first)
        # left_value = cpu_first.split(":")[0]
        cpu_second = temp[1]
        cpu.append(cpu_second)
    return cpu


# cpu use
def get_current_cpu_use():
    out = h.run_cmd("cat /proc/stat|head -n 1")
    l = out.split()
    user = int(l[1])
    nice = int(l[2])
    sys = int(l[3])
    idle = int(l[4])
    current_cpu_use = (user + sys) / (user + nice + sys + idle)
    return current_cpu_use


# thread number
def get_thread_num():
    core_num = h.run_cmd("cat /proc/cpuinfo | grep -c processor")
    free_cpu = 1 - get_current_cpu_use()
    thread_num = int(free_cpu * (int(core_num) - 1))
    return thread_num



def remove_log(log_path):
    if os.path.exists(log_path):
        os.remove(log_path)
    return
