# coding=utf-8
import os
import re
import sys
import time
import threading
from main.item import Item
from utils import decorator
from common import common_value as cv, constants as c

sys.path.append("..")


class HDD_STRESS(Item):
    def __init__(self, info):
        super(HDD_STRESS, self).__init__()
        self.info = info

    def run_item(self):
        self.make_up_raid()
        # self.random_read_write()
        i = 0
        all_data_disks = self.remove_os_disk()
        os_disk = self.get_os_disk()
        write_log0("->>> System Disk is : " + os_disk)
        write_log0("->>> Tatol Non-system Disks: " + str(len(all_data_disks)))
        write_log0("->>> Non-system Disks is : ")
        write_log0(all_data_disks)
        for data_disk in all_data_disks:
            data_disk_t = threading.Thread(target=self.random_read_write, args=(data_disk,str(i)))
            # data_disk_t.setDaemon(True)
            data_disk_t.start()
            i += 1
        return


    # 对每一个非系统盘进行读写测试
    @decorator.item_test
    def random_read_write(self, data_disk, i):
        if int(i) == 0:
            pass
        else:
            cv.remove_log(c.HDD_STRESS_LOG_PATH + "disk" + i + '.log')

        write_log("========= Data Disk NO." + i + " Read And Write Begin  " + get_local_time_string() + " ==========", i)

        shell = "fio -filename={} -direct=1 -iodepth 1" \
                " -thread -rw=randrw -ioengine=psync -bs=16k" \
                " -size=1G -numjobs=10 -runtime={} -group_reporting -time_based" \
                " -name=mytest_{}".format(data_disk, c.RUN_SECONDS, i)
        read_and_write = self.run_cmd(shell)
        # write_log("========== 开始对非系统盘进行读写测试 ==========")
        write_log("The Command Line ->>> " + shell + "\n", i)
        write_log(read_and_write, i)
        write_log("================== Data disk NO." + i +" End ====================", i)
        return read_and_write

    # 对系统盘进行读测试
    @decorator.item_test
    def random_read(self):
        os_disk = self.get_os_disk()
        self.run_cmd("mkdir /test")
        shell = "fio -directory=/test -direct=1 -iodepth 1" \
                " -thread -rw=randread -ioengine=psync -bs=16k -size=1G" \
                " -numjobs=10 -runtime=60 -group_reporting -name=mytest_0"
        write_log("============ System Disk Read Begin  " + get_local_time_string() + " ==============")
        write_log("The Command Line->>> " + shell + "\n")
        os_disk_read = self.run_cmd(shell)
        write_log(os_disk_read)
        write_log("==============  System Disk Read End  " + get_local_time_string() + " =================")
        return os_disk_read

    # 是否要组Raid卡
    def make_up_raid(self):
        cv.remove_log(c.HDD_STRESS_LOG_PATH + "disk0.log")
        write_log0("=========== Disks Read and Write Check  " + get_local_time_string() + " ===============" + "\n")
        raid_or_not = self.run_cmd('lspci | grep "RAID" ')
        if "Fail" in raid_or_not or not raid_or_not:
            # write_log(raid_or_not)
            write_log0("->>> No Raid")
        else:
            write_log0("===================== Building Raid ============================")
            raid = self.run_cmd("cd shell && sh ./makeraid0.sh")
            write_log0("============== Build Raid Success, Information ==================")
            write_log0(raid)
            write_log0("==================================================================")
        return

    # 获取所有sd*,nvme*硬盘
    def get_all_disk(self):
        sd_disk = self.run_cmd('find /dev/ -name "sd*" | grep -E "sd[a-z]$" | sort ')
        nvme_disk = self.run_cmd('find /dev/ -name "nvme*" | grep -E "nvme[0-9][a-z][0-9]$" | sort ')
        if nvme_disk:
            all_disk = sd_disk + "\n" + nvme_disk
        else:
            all_disk = sd_disk
        return all_disk

    # 移除系统盘的所有盘
    def remove_os_disk(self):
        all_disk = self.get_all_disk().split()
        os_disk = self.get_os_disk()
        # print(all_disk)
        for disk in all_disk:
            os_disk_ = re.findall(os_disk, disk)
            for os in os_disk_:
                if os == os_disk:
                    remove_os = "/dev/" + os_disk
                    all_disk.remove(remove_os)
        return all_disk

    # 获取到系统盘
    def get_os_disk(self):
        i = 0
        os_disk = ""
        list_disk = []
        all_disk = self.run_cmd("lsblk")
        disk_list = all_disk.split("\n")
        # print(one_disk)
        for disk in disk_list:
            units = disk.split()
            # print(units)
            list_disk.append(units)
            if len(list_disk[i]) == 7:
                if list_disk[i][-1] == '/boot':
                    os_num = int(list_disk[i][0][-1])
                    os_disk = list_disk[i - os_num][0]
            i += 1

        return os_disk


    # # 检车测试项的log中是否有fail项目
    # def check_log(self):
    #     with open("result.log", "r") as f:
    #         data = f.read()
    #         error1 = re.findall("fail", data)
    #         error2 = re.findall("error", data)
    #         error3 = re.findall("Fail", data)
    #         if error1 or error2 or error3:
    #             write_log("->> 测试项目中有fail项目，请检查！")
    #             # l.log(str(error1) + "\n" + str(error2) + "\n" + str(error3))
    #             return
    #     write_log("->> 测试项目通过测试！")
    #     return


def write_log0(s):
    with open(c.HDD_STRESS_LOG_PATH + 'disk0.log', 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def write_log(s, i):
    with open(c.HDD_STRESS_LOG_PATH + "disk" + i + '.log', 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))
