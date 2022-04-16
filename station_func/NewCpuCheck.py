import re
import sys
import commands
import os
from main.item import Item
from common import constants as c
from utils import decorator, log as l

sys.path.append("..")

CMD_GET_CPU_INFORMATION = 'dmidecode -t 4'
Socket= 'Socket Designation: CPU0'


class Cpu_Check(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.cpu_information_check()


    def cpu_information_check(self):

        cmd='cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l'
        cpu_number=commands.getstatusoutput(cmd)
        write_log('------------ The cpu physical number have %s ------------' % cpu_number[1])
        write_log('------------ cpu info come ------------')
        cmd ='dmidecode -t Processor |grep -i "handle " |awk -F " " \'{print $2}\'|tr -d ","'
        handle=commands.getstatusoutput(cmd)
        # print(handle[1])

        for i in handle[1].split("\n"):
            # print(i)

            cmd='dmidecode -H %s |grep -i "Socket Designation:"' % i
            get_cpu=commands.getstatusoutput(cmd)
            write_log(get_cpu[1])

            cmd='dmidecode -H %s |grep -i "Version: "' % i
            get_cpu_mandufact=commands.getstatusoutput(cmd)
            write_log(get_cpu_mandufact[1])
            cmd = 'dmidecode -H %s |grep -i "Current Speed:"' %i
            get_cpu_speed =commands.getstatusoutput(cmd)
            write_log(get_cpu_speed[1])
            cmd = 'cat /proc/cpuinfo| grep "cpu cores"| uniq'
            get_cpu_core=commands.getstatusoutput(cmd)
            write_log('       The cpu core number is %s' %get_cpu_core[1] )
            cmd = 'dmidecode -H %s |grep -i "Thread Count: "' % i
            get_cpu_thread = commands.getstatusoutput(cmd)
            write_log(get_cpu_thread[1])
            write_log('------------ The cpu is ok next is coming ------------')



            # for line in get_cpu[1].split('\n'):
            #     if re.search(Socket,line,re.IGNORECASE):
            #         write_log('this is cpu0')


def write_log(s):
    with open(c.Check_hw_info, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)




