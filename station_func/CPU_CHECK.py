# coding=utf-8
import re
import sys
from main.item import Item
from utils import decorator, log as l
from common import common_value
sys.path.append("..")

###############
# Command
##############

# CPU信息
CMD_GET_CPU_INFORMATION = 'dmidecode -t 4'

"""
# CPU数量校验
CMD_GET_CPU_NUMBER = 'dmidecode -t 4 | grep "Socket Designation" '

# CPU核数校验
CMD_GET_CPU_CORE_NUMBER = 'dmidecode -t 4 | grep "Core Count" '

# CPU型号校验
CMD_GET_CPU_TYPE = 'dmidecode -t 4 | grep "Version" '

# CPU主频校验
CMD_GET_CPU_FREQUENCY = 'dmidecode -t 4 | grep "Current Speed" '
"""

# CPU负载测试
CMD_GET_CPU_STRESS = 'stress -c 8 -t 10'

# CPU MCE检测
CMD_GET_CPU_MCE = 'ras-mc-ctl --summary'


class CPU_CHECK(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.cpu_information_check()
        # self.cpu_number_check()
        # self.cpu_core_number_check()
        # self.cpu_type_check()
        # self.cpu_frequency_check()
        self.cpu_loading_check()
        self.cpu_mce_check()

    # CPU信息查询
    # @decorator.item_test
    def cpu_information_check(self):
        cpu_information = self.run_cmd(CMD_GET_CPU_INFORMATION)
        l.write_debug_log(cpu_information)
        cpu_number_list = re.findall(r'(Socket Designation: (.*))', cpu_information)
        # l.log("==========CPU数量校验===========")
        cpu_number_list_ = common_value.get_cpu_information(cpu_number_list)
        cpu_number = len(set(cpu_number_list_))
        l.log(">>> " + str(cpu_number))

        cpu_core_number_list = re.findall(r'(Core Count: (.*))', cpu_information)
        cpu_core_counts = 0
        # l.log("==========CPU核数校验============")
        cpu_core_number_list_ = common_value.get_cpu_information(cpu_core_number_list)
        for number in cpu_core_number_list_:
            cpu_core_counts += int(number)
        l.log(">>> " + str(cpu_core_counts))

        cpu_type_list = re.findall(r'(Version: (.*))', cpu_information)
        # l.log("===========CPU型号校验===========")
        cpu_type_list_ = common_value.get_cpu_information(cpu_type_list)
        cpu_version = set(cpu_type_list_)
        for type in cpu_version:
            l.log(">>> " + type)

        cpu_frequency_list = re.findall(r'(Current Speed: (.*))', cpu_information)
        # l.log("==========CPU主频校验=============")
        cpu_frequency_list_ = common_value.get_cpu_information(cpu_frequency_list)
        for frequency in cpu_frequency_list_:
            l.log(">>> " + frequency)
        # l.log("=================================")

    """
    # CPU数量
    @decorator.item_test
    def cpu_number_check(self):
        cpu_socket = self.run_cmd(CMD_GET_CPU_NUMBER)
        l.log(cpu_socket)
        cpu_number_list = self.get_cpu_information(cpu_socket)
        cpu_number = len(set(cpu_number_list))
        l.log("========  CPU的数量为：" + str(cpu_number) + "  =========")
        # print(cpu_number)
        return cpu_number

    # CPU核数校验
    @decorator.item_test
    def cpu_core_number_check(self):
        core_counts = 0
        cpu_core = self.run_cmd(CMD_GET_CPU_CORE_NUMBER)
        l.log(cpu_core)
        cpu_core_list = self.get_cpu_information(cpu_core)
        for count in cpu_core_list:
            core_counts += int(count)
        l.log("========  CPU核数为：" + str(core_counts) + "  =========")
        return core_counts

    # CPU型号校验
    @decorator.item_test
    def cpu_type_check(self):
        cpu_type_ = self.run_cmd(CMD_GET_CPU_TYPE)
        l.log(cpu_type_)
        cpu_type_list = self.get_cpu_information(cpu_type_)
        cpu_types = set(cpu_type_list)
        l.log("========  CPU的型号 ========")
        for cpu_type in cpu_types:
            l.log(cpu_type)
        l.log("===========================")
        return cpu_type

    # CPU主频校验
    @decorator.item_test
    def cpu_frequency_check(self):
        cpu_frequency = self.run_cmd(CMD_GET_CPU_FREQUENCY)
        l.log(cpu_frequency)
        cpu_frequency_list = self.get_cpu_information(cpu_frequency)
        l.log("========  CPU的主频 ========")
        l.log(cpu_frequency_list)
        l.log("===========================")
        return cpu_frequency_list
    """

    # CPU负载测试
    @decorator.item_test
    def cpu_loading_check(self):
        # 安装CPU负载测试工具
        self.run_cmd("cd tools && sh stress.sh")
        stess_display = self.run_cmd(CMD_GET_CPU_STRESS)
        l.log("========  CPU的负载测试 ========")
        l.log(stess_display)
        l.log("================================")
        return stess_display

    # CPU MCE检测
    @decorator.item_test
    def cpu_mce_check(self):
        # 安装CPU MEC检测工具
        self.run_cmd("cd tools && sh rasdaemon.sh")
        cpu_mec_display = self.run_cmd(CMD_GET_CPU_MCE)
        l.log("========  CPU MCE检测 ===========")
        l.log(cpu_mec_display)
        l.log("================================")
        self.cpu_mce_errors(cpu_mec_display)
        return cpu_mec_display

    # CPU MCE 检测出现错误
    def cpu_mce_errors(self, mce_errors):
        temp = mce_errors.split('\n')
        for mce in temp:
            if mce == '':
                continue
            result = re.match("No", mce)
            if not result:
                errors_information = self.run_cmd("ras-mc-ctl --errors")
                l.log("========= CPU MCE 检测出现错误============")
                l.log(errors_information)
                l.log("========================================")
                return errors_information


