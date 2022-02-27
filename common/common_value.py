# coding=utf-8
from utils import log as l
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
    # return cpu, left_value


def remove_log(log_path):
    if os.path.exists(log_path):
        os.remove(log_path)
    else:
        pass







