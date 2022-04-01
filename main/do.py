import json, sys
import controller
from common import constants as c

sys.path.append("..")
from station_func import HOST_CFG_SET, INFO_PROGRAMMING, RTC_CHECK, NewCpuCheck, NewMemCheck, VENEER_HEALTH_CHECK, NewHddCheck, NewNetworkCheck, AllContrast, \
    MAC_ADDRESS_CHECK
from station_stress import CPU_STRESS, MEM_STRESS
from station_stress import HDD_STRESS, STRESS_ALL, LAN_STRESS, MCE_ECC
from station_final import LOG_CLEAN_TEST
from station_stress import BlackListCheck

def do(station_name, item):
    if station_name == 'STATION_FUNC':
        name = item['name']
        if name == 'RTC_CHECK':
            RTC_CHECK.RTC_CHECK(item).run_item()
        if name == 'HOST_CFG_SET':
            HOST_CFG_SET.HOST_CFG_SET(item).run_item()
        if name == 'INFO_PROGRAMMING':
            INFO_PROGRAMMING.INFO_PROGRAMMING(item).run_item()
        if name == 'NewCpuCheck':
            NewCpuCheck.Cpu_Check(item).run_item()
        if name == 'NewMemCheck':
            NewMemCheck.Mem_Check(item).run_item()
        if name == 'VENEER_HEALTH_CHECK':
            VENEER_HEALTH_CHECK.VENEER_HEALTH_CHECK(item).run_item()
        if name == 'MAC_ADDRESS_CHECK':
            MAC_ADDRESS_CHECK.MAC_ADDRESS_CHECK(item).run_item()
        if name == 'NewHddCheck':
            NewHddCheck.Hdd_Check(item).run_item()
        if name == 'NewNetworkCheck':
            NewNetworkCheck.Network_Check(item).run_item()
        if name == 'AllContrast':
            AllContrast.cmpFile('/home/hw_stress/compare/peizhibijiao.log', c.Check_hw_info ).run_item()

    elif station_name == 'STATION_STRESS':
        name = item['name']
        if name == 'STRESS_ALL':
            STRESS_ALL.STRESS_ALL(item).run_item()
        if name == 'MCE_ECC':
            MCE_ECC.MCE_ECC(item).run_item()
        if name == 'CPU_STRESS':
            CPU_STRESS.CPU_STRESS(item).run_item()
        if name == 'MEM_STRESS':
            MEM_STRESS.MEM_STRESS(item).run_item()
        if name == 'HDD_STRESS':
            HDD_STRESS.HDD_STRESS(item).run_item()
        if name == 'LAN_STRESS':
            LAN_STRESS.LAN_STRESS(item).run_item()
        if name == 'BlackListCheck':
            BlackListCheck.BlackListCheck(item).run_item()


    else:
        name = item['name']
        if name == 'LOG_CLEAN_TEST':
            LOG_CLEAN_TEST.LOG_CLEAN_TEST(item).run_item()
