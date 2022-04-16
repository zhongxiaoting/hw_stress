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


class Mem_Check(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.mem_information_check()

    def mem_information_check(self):
        cmd = 'dmidecode -t memory | grep -A 11 -B 5 "Size:.*GB" | grep \'Size:.*GB\' | wc -l '
        mem_number = commands.getstatusoutput(cmd)
        write_log('------------ The memory physical number have %s ------------' % mem_number[1])
        write_log('------------ mem info come ------------')
        cmd = 'dmidecode -t 17 |grep -i "handle " |awk -F " " \'{print $2}\'|tr -d ","'
        handle = commands.getstatusoutput(cmd)

        for i in handle[1].split("\n"):
            cmd = 'dmidecode -H %s |grep -i "Locator: "' % i
            get_mem = commands.getstatusoutput(cmd)
            write_log(get_mem[1])
            cmd = 'dmidecode -H %s |grep -i "Manufacturer: "' % i
            get_mem_mandufact = commands.getstatusoutput(cmd)
            write_log(get_mem_mandufact[1])
            cmd = 'dmidecode -H %s |grep -i "Speed:"' % i
            get_mem_speed = commands.getstatusoutput(cmd)
            write_log(get_mem_speed[1])
            cmd = 'dmidecode -H %s |grep -i "Serial Number: "' % i
            get_mem_SN = commands.getstatusoutput(cmd)
            write_log(get_mem_SN[1])
            cmd = 'dmidecode -H %s |grep -i "Part Number: "' % i
            get_mem_PN = commands.getstatusoutput(cmd)
            write_log(get_mem_PN[1])
            write_log('------------ The memory is ok next is coming ------------')

            # for line in get_cpu[1].split('\n'):
            #     if re.search(Socket,line,re.IGNORECASE):
            #         write_log('this is cpu0')


def write_log(s):
    with open(c.Check_hw_info, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)