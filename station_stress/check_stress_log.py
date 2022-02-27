# coding=utf-8
import os
import re
import sys
import time
from common import constants as c
from station_stress import LOSS_DISK
from utils import handle as h
from utils import log as l
from station_stress import HDD_STRESS
from main.item import Item


class ALL_STRESS_LOG():

    def run_item(self):
        # self.backup_log()
        while True:
            stress = LOSS_DISK.stress_run()
            memtester = LOSS_DISK.mem_run()
            fio = LOSS_DISK.fio_run()
            lan = LOSS_DISK.lan_run()
            if stress is None and memtester is None and fio is None and lan is None:
                # print("check_stress->> " + str(stress) + "   memtester->> " + str(memtester)
                #       + "   fio->> " + str(fio))
                self.read_cpu_log()
                self.read_mem_log()
                self.read_hdd_log()
                self.read_lan_log()
                self.check_log()
                break

    # backup stress.log
    def backup_log(self):
        if os.path.exists(c.STRESS_ALL_LOG):
            if not os.path.exists(c.STRESS_LOG + '/backup'):
                h.run_cmd('cd %s && mkdir backup' % (c.STRESS_LOG))
            os.rename(c.STRESS_ALL_LOG, c.STRESS_LOG + '/backup/' + self.get_local_time_string() + '.log')

    def read_cpu_log(self):
        with open(c.CPU_STRESS_LOG_PATH, "r") as f:
            cpu_data = f.read()
            self.check_log("CPU", cpu_data)
        self.write_log("===============  STRESS_ALL " + self.get_local_time_string() + "=======================")
        self.write_log(cpu_data)
        return cpu_data

    def read_mem_log(self):
        with open(c.MEM_STRESS_LOG_PATH, "r") as f:
            mem_data = f.read()
            self.check_log("Memory", mem_data)
        self.write_log(str(mem_data) + '\n')
        return mem_data

    def read_hdd_log(self):
        data_disks = HDD_STRESS.HDD_STRESS(Item).remove_os_disk()
        len_disks = len(data_disks)
        for i in range(len_disks):
            with open(c.HDD_STRESS_LOG_PATH + "disk" + str(i) + '.log', "r") as f:
                hdd_data = f.read()
                self.check_log("disk" + str(i), hdd_data)
            self.write_log(str(hdd_data) + '\n')
        return hdd_data

    def read_lan_log(self):
        with open(c.LAN_STRESS_LOG_PATH, "r") as f:
            lan_data = f.read()
            self.check_log("Network Card", lan_data)
        self.write_log(str(lan_data) + '\n')
        return lan_data

    def write_log(self, s):
        with open(c.STRESS_ALL_LOG, 'a+') as f:
            f.write(str(s) + '\n')
            f.flush()
            os.fsync(f)

    # 检查测试项的log中是否有fail项目
    def check_log(self, name, data):
        error1 = re.findall("fail", data)
        error2 = re.findall("Fail", data)
        error3 = re.findall("error", data)
        error4 = re.findall("ERROR", data)
        if error1 or error2 or error3 or error4:
            self.write_log("->> There are ERRORS in the project, Please check！")
            l.fail_msg("{} Check have ERROR, Please check progress!".format(name))
            sys.exit(0)
            return
        self.write_log("->> PASS ！")
        return


def get_local_time_string(self):
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# if __name__ == "__main__":
#     check = ALL_STRESS_LOG()
#     check.run_item()
