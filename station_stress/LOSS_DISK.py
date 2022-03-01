# coding=utf-8
import os
import sys
import time
from time import sleep
from utils import handle as h, log as l
from common import common_value as cv, constants as c
from main.item import Item


class LOSS_DISK(Item):
    def __init__(self, info):
        super(LOSS_DISK, self).__init__()
        self.info = info

    # 检查掉盘测试
    def run_item(self):
        i = 1
        sleep(300)
        disks = self.get_disk()
        write_log("==============  Loss Disk Check Begin " + get_local_time_string() + " =================")
        while True:
            fio = fio_run()
            memtester = mem_run()
            stress = stress_run()
            lan = lan_run()
            # print("stress->> " + str(stress) + "   memtester->> " + str(memtester) + "   fio->> "
            #           + str(fio))
            if stress and memtester and fio and lan:
                write_log("->>> CPU、Memory、Disks、LAN Stress Check is Running...")
                loss_or_not_disk = h.run_cmd("lsblk")
                write_log("->>> Disks Showing : ")
                write_log(loss_or_not_disk)
                if disks == loss_or_not_disk:
                    write_log("->>> Not Loss Disks! ")
                else:
                    write_log("->>>ERROR, Disks Loss! ")
                    l.fail_msg("Disk Loss Check have ERROR, Please check progress!")
                    self.stress_fail()
                    break
            # when all stress is None, stress check is finished
            elif stress is None and memtester is None and fio is None and lan is None:
                write_log("->> stress、memtester 、fio and lan stress check are finished!")
                break
            write_log("=========== NO_" + str(i) + " Loss Disk Check End " + get_local_time_string() + "  ===========")
            i += 1
            sleep(c.LOSS_DISK_TIME)
        return

    def get_disk(self):
        disks = h.run_cmd("lsblk")
        return disks


def stress_run():
    stress = h.run_cmd("pidof stress")
    if "Fail" in stress:
        return None
    return stress


def mem_run():
    memtester = h.run_cmd("pidof memtester")
    if "Fail" in memtester:
        return None
    return memtester


def fio_run():
    fio = h.run_cmd("pidof fio")
    if "Fail" in fio:
        return None
    return fio


def lan_run():
    lan = h.run_cmd("pidof lan_while.sh")
    if "Fail" in lan:
        return None
    return lan


def write_log(s):
    with open(c.LOSS_DISK_LOG_PATH, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)




def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))
