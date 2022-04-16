import re
import sys
import commands
import os
from main.item import Item
from common import constants as c
from utils import decorator, log as l

sys.path.append("..")

CMD_GET_CPU_INFORMATION = 'dmidecode -t 4'
Socket = 'Socket Designation: CPU0'


class Hdd_Check(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.hdd_information_check()
        self.nvme_information_check()

    def nvme_information_check(self):
        cmd = 'ls /sys/block |grep -Ev "loop*|ram*|sd*|dm"'

        nvme_name = commands.getstatusoutput(cmd)
        if len(nvme_name[1]) != 0:
            write_log("------------ The nvme count is %s ------------" % len(nvme_name[1]))
            for xxl in nvme_name[1].split("\n"):


                write_log("------------ This nvme is %s ------------" % xxl)

                cmd = 'smartctl -a /dev/%s |grep -i "Device Model:"' % (xxl)
                get_nvme_base_info = commands.getstatusoutput(cmd)
                write_log(get_nvme_base_info[1])
                cmd = 'smartctl -a /dev/%s |grep -i "User Capacity:"' % (xxl)
                get_nvme_capacity=commands.getstatusoutput(cmd)
                write_log(get_nvme_capacity[1])
                cmd = 'smartctl -a /dev/%s |grep -i "Serial number:"' %(xxl)
                get_nvme_SN=commands.getstatusoutput(cmd)
                write_log(get_nvme_SN[1])
                write_log('------------ This nvme is ok next coming ------------' )
                # nvme_info = nvme_info[1].split('\n')
        else:
            write_log('Can not find any nvme.')

    def hdd_information_check(self):
        pgone = 'SMART overall-health self-assessment test result: PASSED'
        SAS = 'Transport protocol:   SAS (SPL-3)'
        SAS_h = 'SMART Health Status: OK'
        cmd = 'lspci |grep -i "raid"'
        look_raid = commands.getstatusoutput(cmd)

        if len(look_raid[1]) != 0:
            # print(look_raid)
            panfu_list = []
            yingpan_list = []
            yp_info = []
            # nvme_name=[]

            cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -LdPdInfo -aALL | grep "Device Id:"'
            raid_hdd_number = self.run_cmd(cmd).split('\n')

            cmd = 'ls /sys/block |grep -Ev "loop*|ram*|nvme|dm"'
            raid_hdd_name = self.run_cmd(cmd).split('\n')

            if len(raid_hdd_name) != 0:
                raid_hdd_number_count=len(raid_hdd_name)
                write_log('------------ The hdd number count is %s ------------' %raid_hdd_number_count )

                for i in raid_hdd_number:
                    panfu = i.split()[2]
                    panfu = int(panfu)
                    panfu_list.append(panfu)
                # much=len(panfu_list)

                for i in raid_hdd_name:
                    yingpan = i.split()[0]
                    yingpan_list.append(yingpan)

                # for num in range(0, len(dev_info)):

                for i in range(0, len(panfu_list)):
                    write_log("------------ This hdd is %s ------------" % yingpan_list[i])
                    # cmd = "cat /var/log/messages"
                    # msg_info = commands.getstatusoutput(cmd)
                    cmd = 'smartctl -a -d megaraid,%d /dev/%s |grep -i "Device Model:"' % (panfu_list[i], yingpan_list[i])
                    yp_info = commands.getstatusoutput(cmd)
                    write_log(yp_info[1])
                    # sn=re.findall(r'(Serial Number:(.*))',yp_info[1])
                    cmd = 'smartctl -a -d megaraid,%d /dev/%s |grep -i "Serial number:"' % (panfu_list[i], yingpan_list[i])
                    hdd_sn = commands.getstatusoutput(cmd)
                    write_log(hdd_sn[1])
                    cmd = 'smartctl -a -d megaraid,%d /dev/%s |grep -i "User Capacity:"' % (panfu_list[i], yingpan_list[i])
                    get_hdd_capacity = commands.getstatusoutput(cmd)
                    write_log(get_hdd_capacity[1])
                    write_log('------------ This hdd is ok next coming ------------')

            else:
                write_log("cannot find the hdd and ssd,pleace check about and check about raid what happen")

        else:
            write_log("------------ This type server is no raid ------------")
            cmd = 'ls /sys/block |grep -Ev "loop*|ram*|nvme|dm"'
            hdd_name = self.run_cmd(cmd).split('\n')
            if len(hdd_name) != 0:
                panduan = False
                no_raid_hdd_count = len(hdd_name)
                write_log('The hdd number count is %s' %no_raid_hdd_count)
                for i in hdd_name:
                    write_log('------------ This hdd is %s ------------' %i)
                    cmd = 'smartctl -a /dev/%s |grep -i "Device Model:"' % i
                    no_raid_yp_info = commands.getstatusoutput(cmd)
                    write_log(no_raid_yp_info[1])
                    cmd = 'smartctl -a /dev/%s |grep -i "Transport protocol:   SAS"' % i
                    sas_type = commands.getstatusoutput(cmd)
                    if len(sas_type[1]) != 0:
                        write_log(sas_type[1])
                    else:
                        pass
                    cmd = 'smartctl -a /dev/%s |grep -i "Vendor:"' % i
                    no_raid_yp_Vendor = commands.getstatusoutput(cmd)
                    if len(no_raid_yp_Vendor[1]) !=0:
                        write_log(no_raid_yp_Vendor[1])
                    else:
                        pass
                    cmd = 'smartctl -a /dev/%s |grep -i "Serial number:"' % i
                    no_raid_yp_sn = commands.getstatusoutput(cmd)
                    write_log(no_raid_yp_sn[1])
                    cmd = 'smartctl -a /dev/%s |grep -i "User Capacity:"' % (i)
                    no_raid_yp_capacity = commands.getstatusoutput(cmd)
                    write_log(no_raid_yp_capacity[1])
                    write_log('------------ This hdd is ok next coming ------------')


            else:
                write_log("------------ cannot find the hdd and ssd,pleace check about ------------")


def write_log(s):
    with open(c.Check_hw_info, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)