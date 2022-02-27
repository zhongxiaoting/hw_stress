#-*- coding: UTF-8 -*-
import re

import utils.log as l
from main.item import Item
from common import common_value

CMD_GET_DISK1 = 'sudo smartctl -a /dev/sde'
CMD_GET_DISK2 = 'sudo smartctl -i /dev/sdd'

class DISK_CHECK(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.disk1_check()
        self.disk2_check()
        self.disk_read_write()
        self.disk_longdst()
        self.disk_transducer()

    def disk1_check(self):
        disk_information1 = self.run_cmd(CMD_GET_DISK1)
        l.write_debug_log(disk_information1)
        print(disk_information1)
        disk1_list = re.findall(r'(Device Model:     (.*))', disk_information1)

        # disk1, left_value = common_value.get_cpu_information(disk1_list)
        disk1 = common_value.get_cpu_information(disk1_list)
        # with open('/home/abc/Desktop/test2/check.json') as f:
        #     a = f.read()
        #     b = json.loads(a)
        #     print(b[left_value] == disk1[0])
            # print(a[left_value])
        l.log(">>> " + disk1[0])

    # TODO
    def disk2_check(self):
        disk_information2 = self.run_cmd(CMD_GET_DISK2)
        l.write_debug_log(disk_information2)
        disk2_list1 = re.findall(r'(Vendor:               (.*))', disk_information2)
        disk2_list2 = re.findall(r'(Product:              (.*))', disk_information2)
        disk2 = common_value.get_cpu_information(disk2_list1)
        disk2_ = common_value.get_cpu_information(disk2_list2)
        l.log(">>> " + disk2[0])
        l.log(">>> " + disk2_[0])


    # 硬盘读写测试
    def disk_read_write(self):
        fio_information = self.run_cmd("cd tools && sh fio.sh")
        l.write_debug_log(fio_information)
        l.log(fio_information)

    # 硬盘LongDST测试
    def disk_longdst(self):
        longdst = self.run_cmd("cd tools && sh smartctl.sh")
        l.write_debug_log(longdst)
        l.log(longdst)

    # 硬盘smart信息，传感器测试
    # TODO
    def disk_transducer(self):
        transducer_info = self.run_cmd("cd tools && transducer.sh")
        l.write_debug_log(transducer_info)
        l.log(transducer_info)



