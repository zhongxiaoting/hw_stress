import json, sys
import controller

sys.path.append("..")
from station_func import HOST_CFG_SET, INFO_PROGRAMMING, RTC_CHECK, CPU_CHECK, DISK_CHECK, VENEER_HEALTH_CHECK, \
    MAC_ADDRESS_CHECK
from station_stress import CPU_STRESS, MEM_STRESS
from station_stress import HDD_STRESS, STRESS_ALL, LAN_STRESS, MCE_ECC
from station_final import LOG_CLEAN_TEST
from station_func import BlackListCheck

def do(station_name, item):
    if station_name == 'STATION_FUNC':
        name = item['name']
        if name == 'RTC_CHECK':
            RTC_CHECK.RTC_CHECK(item).run_item()
        if name == 'HOST_CFG_SET':
            HOST_CFG_SET.HOST_CFG_SET(item).run_item()
        if name == 'INFO_PROGRAMMING':
            INFO_PROGRAMMING.INFO_PROGRAMMING(item).run_item()
        if name == 'CPU_CHECK':
            CPU_CHECK.CPU_CHECK(item).run_item()
        if name == 'DISK_CHECK':
            DISK_CHECK.DISK_CHECK(item).run_item()
        if name == 'VENEER_HEALTH_CHECK':
            VENEER_HEALTH_CHECK.VENEER_HEALTH_CHECK(item).run_item()
        if name == 'MAC_ADDRESS_CHECK':
            MAC_ADDRESS_CHECK.MAC_ADDRESS_CHECK(item).run_item()
        if name == 'BlackListCheck':
            BlackListCheck.ItemBlacklistCheck(item).run_item()
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


    else:
        name = item['name']
        if name == 'LOG_CLEAN_TEST':
            LOG_CLEAN_TEST.LOG_CLEAN_TEST(item).run_item()
