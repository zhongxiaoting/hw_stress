import re
import sys
import commands
import os
from main.item import Item
from common import constants as c
from utils import decorator, log as l

sys.path.append("..")

network_port_look='logical name:'
getout_virb = 'logical name: virbr0'

class Network_Check(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.network_information_check()
        self.pci_count_check()

#lspci |grep -i "eth" |awk -F " " '{for(i=2;i<=NF;++i)printf $i "\t";printf "\n"}' | uniq |wc -l
    def network_information_check(self):
        cmd = 'lspci |grep -i "eth" |awk -F " " \'{$1 ="";print}\' | uniq |wc -l'
        cmd_network_count=commands.getstatusoutput(cmd)
        write_log('------------ The network number is %s ------------' % cmd_network_count[1])
        cmd = 'lshw -class network > %s' %(c.Network_info)
        cmd_network_info = commands.getstatusoutput(cmd)
        get_all_network_info=open(c.Network_info)
        read_all_network_info=get_all_network_info.read()
        read_all_network_info=read_all_network_info.split('*-network:')
        for i in read_all_network_info:
            for line in i.split('\n'):
                if re.search(network_port_look,line,re.IGNORECASE):
                    if not re.search(getout_virb,line,re.IGNORECASE):

                        write_log(line)
                        network_product_name = re.findall(r'product: (.*)',i)
                        write_log(network_product_name[0])
                        network_vendor = re.findall(r'vendor: (.*)',i)
                        write_log(network_vendor[0])
                        network_speed = re.findall(r'size: (.*)', i)
                        if len(network_speed) != 0:
                            write_log(network_speed[0])
                        else:
                            pass

                        write_log("------------ next one -------------")


    def pci_count_check(self):
        cmd= 'lspci |wc -l'
        all_pci_count = commands.getstatusoutput(cmd)

        write_log('------------ The pci number is %s ------------'%all_pci_count[1])






def write_log(s):
    with open(c.Check_hw_info, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)