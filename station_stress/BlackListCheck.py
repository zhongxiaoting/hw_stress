# coding=utf-8
import commands
import os
import re
import sys
from main.item import Item
from common import constants as c
from utils import decorator, log as l
from common import common_value
import time
from station_stress.MCE_ECC import MCE_ECC

sys.path.append("..")


class BlackListCheck(Item):

    def __init__(self, info):
        super(BlackListCheck, self).__init__()
        self.info = info
        self.finished = False
        self.results = {}

    def run_item(self):
        self.report_info('S')
        self.check_hdd()
        write_log("------------------------------------------------")
        self.check_nvme()
        write_log("------------------------------------------------")
        self.check_mcelog()
        write_log("------------------------------------------------")
        self.check_ethernet_errors()
        write_log("------------------------------------------------")
        self.check_PCIE_errors()
        write_log("------------------------------------------------")
        self.check_SEL()
        write_log("------------------------------------------------")
        self.look_ecc()
        write_log("-----------end----------------------------------")
        if len(self.results) == 0:
            self.report_info('P')
            # self.on_pass()
            write_log("ALL GOOD")
        else:
            self.report_info('F')
            write_log(self.results)
            self.on_fail()
        self.finished = True

    def check_nvme(self):
        # cmd = 'lspci |grep -i "raid"'
        # all = commands.getstatusoutput(cmd)
        nvme_name = []
        cmd = 'ls /sys/block |grep -Ev "loop*|ram*|sd*|dm"'

        nvme_name = commands.getstatusoutput(cmd)
        if len(nvme_name[1]) != 0:
            for nv in nvme_name[1].split("\n"):

                write_log("the check nvme is go,this is :%s" % nv)

                cmd = 'nvme smart-log /dev/%s' % nv
                nvme_info = commands.getstatusoutput(cmd)
                nvme_info = nvme_info[1].split('\n')
                CW = re.findall(r'(critical_warning(.*))', nvme_info[1])
                if len(CW)!=0:
                    x = CW[0][1].split()[-1]
                    x = int(x)
                    if x == 0:
                        write_log('critical_warning is OK')
                    else:
                        write_log("critical_warning is fail")
                        self.results['nvme_log'] = 'fail'
                        self.result_fail()
                else:
                    write_log("cannot find critical_warning")

                cmd = 'nvme smart-log /dev/%s |grep -i "available_spare                     :"' % nv
                AS = commands.getstatusoutput(cmd)
                x = AS[1].split(":")
                x = x[1].strip()
                # print(x)
                x = str(x)
                if x == '100%' or x == '99%':
                    write_log('available_spare is OK')
                else:
                    write_log("available_spare is fail")
                    self.results['nvme_log'] = 'fail'
                    self.result_fail()

                cmd = 'nvme smart-log /dev/%s |grep -i "percentage_used"' % nv

                PU = commands.getstatusoutput(cmd)
                # print(PU)

                PU = re.findall(r'(percentage_used(.*))', PU[1])
                if len(PU)!=0:
                    x = PU[0][1].split()[-1]
                    if x == '0%':
                        write_log('percentage_used is OK')
                    else:
                        write_log("percentage_used is fail")
                        self.results['nvme_log'] = 'fail'
                        self.result_fail()
                else:
                    write_log("cannot find percentage_used")

        else:
            write_log("cannot find the nvme,please check about.")

    def check_hdd(self):
        health_status = 'SMART overall-health self-assessment test result: PASSED'
        SAS = 'Transport protocol:   SAS (SPL-3)'
        SAS_h = 'SMART Health Status: OK'
        cmd = 'lspci |grep -i "raid"'
        cat_raid = commands.getstatusoutput(cmd)

        if len(cat_raid[1]) != 0:
            #print(cat_raid)
            panfu_list = []
            yingpan_list = []
            yp_info = []
            # nvme_name=[]

            cmd = '/home/hw_stress/tools/MegaCli64 -LdPdInfo -aALL | grep -i "Device Id:" |grep -Ev "Enclosure"'
            hdd_number = self.run_cmd(cmd).split('\n')

            cmd = 'ls /sys/block |grep -Ev "loop*|ram*|nvme|dm"'
            hdd_name = self.run_cmd(cmd).split('\n')

            if len(hdd_name) != 0:

                for i in hdd_number:
                    # print(i)
                    panfu = i.split(':')[1].strip()
                    #print(panfu)
                    panfu_list.append(panfu)

                for i in hdd_name:
                    yingpan = i.split()[0]
                    yingpan_list.append(yingpan)

                for i in range(0, len(panfu_list)):
                    panduan = False
                    # cmd = "cat /var/log/messages"
                    # msg_info = commands.getstatusoutput(cmd)
                    cmd = 'smartctl -a -d megaraid,%s /dev/%s' % (panfu_list[i], yingpan_list[i])
                    yp_info = commands.getstatusoutput(cmd)
                    cmd = 'smartctl -a -d megaraid,%s /dev/%s |grep -i "Serial number:"' % (
                        panfu_list[i], yingpan_list[i])
                    sn = commands.getstatusoutput(cmd)
                    for line in yp_info[1].split('\n'):
                        if re.search(health_status, line, re.IGNORECASE):
                            write_log('the check hdd is go :SMART overall-health self-assessment test result: PASSED')
                            panduan = True

                        else:
                            pass

                    if panduan == True:
                        write_log(sn[1])
                        RS = re.findall(r'(Reallocated_Sector_Ct(.*))', yp_info[1])
                        if len(RS) != 0:
                            x = RS[0][1].split()[-1]
                            x = int(x)
                            if x <= 10:
                                write_log('Reallocated_Sector_Ct is OK')
                            else:
                                write_log(sn[1])
                                write_log("Reallocated_Sector_Ct is fail")
                                self.results['hdd_log'] = 'fail'
                                self.result_fail()
                        else:
                            write_log("cannot find Reallocated_Sector_Ct")

                        EE = re.findall(r'(End-to-End_Error(.*))', yp_info[1])
                        if len(EE) != 0:
                            x = EE[0][1].split()[-1]
                            x = int(x)
                            if x == 0:
                                write_log("End-to-End_Error is OK")
                            else:
                                write_log(sn[1])
                                write_log("End-to-End_Error is fail")
                                self.results['hdd_log'] = 'fail'
                                # result_fail(self)
                                self.result_fail()
                        else:
                            write_log('cannot find End-to-End_Error')

                        CP = re.findall(r'(Current_Pending_Sector(.*))', yp_info[1])
                        if len(CP) != 0:
                            x = CP[0][1].split()[-1]
                            x = int(x)
                            if x == 0:
                                write_log("Current_Pending_Sector is OK")
                            else:
                                write_log(sn[1])
                                write_log("Current_Pending_Sector is fail")
                                self.results['hdd_log'] = 'fail'
                                self.result_fail()
                        else:
                            write_log("cannot find Current_Pending_Sector")

                    else:
                        write_log(sn[1])
                        write_log("SMART overall-health self-assessment test result is fail")
                        self.results['hdd_log'] = 'fail'
                        self.result_fail()

            else:
                write_log("cannot find the hdd and ssd,pleace check about")
        else:
            cmd = 'ls /sys/block |grep -Ev "loop*|ram*|nvme|dm"'
            hdd_name = self.run_cmd(cmd).split('\n')
            if len(hdd_name) != 0:

                for i in hdd_name:
                    panduan = False
                    print(i)
                    cmd = 'smartctl -a /dev/%s' % i
                    yp_info = commands.getstatusoutput(cmd)
                    cmd = 'smartctl -a /dev/%s |grep -i "Transport protocol:   SAS"' % i
                    look_sas_hdd = commands.getstatusoutput(cmd)
                    cmd = 'smartctl -a /dev/%s |grep -i "Serial number:"' % i
                    sn = commands.getstatusoutput(cmd)
                    if len(look_sas_hdd[1]) != 0:
                        # write_log(wtf)
                        write_log("this hdd is SAS:%s" % i)
                        for line in yp_info[1].split('\n'):
                            if re.search(SAS_h, line, re.IGNORECASE):
                                write_log('the check SAS hdd is go :SMART Health Status: OK')
                                panduan = True
                            else:
                                pass
                        if panduan == True:
                            write_log(sn[1])
                            EL = re.findall(r'(Elements in grown defect list:(.*))', yp_info[1])
                            if len(EL) != 0:
                                x = EL[0][1].split()[-1]
                                x = int(x)
                                if x <= 5:
                                    write_log('Elements in grown defect list is OK')
                                else:
                                    write_log(sn[1])
                                    write_log("Elements in grown defect list is fail")
                                    self.results['hdd_log'] = 'fail'
                                    # result_fail(self)
                                    self.result_fail()
                            else:
                                write_log("cannot find Elements in grown defect list")

                    else:
                        for line in yp_info[1].split('\n'):
                            if re.search(health_status, line, re.IGNORECASE):
                                write_log(
                                    'the check hdd is go :SMART overall-health self-assessment test result: PASSED')
                                panduan = True

                            else:
                                pass
                        if panduan == True:
                            write_log(sn[1])
                            RS = re.findall(r'(Reallocated_Sector_Ct(.*))', yp_info[1])
                            if len(RS) != 0:

                                x = RS[0][1].split()[-1]
                                x = int(x)
                                if x <= 10:
                                    write_log('Reallocated_Sector_Ct is OK')
                                else:
                                    write_log(sn[1])
                                    write_log("Reallocated_Sector_Ct is fail")
                                    self.results['hdd_log'] = 'fail'
                                    # result_fail(self)
                                    self.result_fail()
                            else:
                                write_log("cannot find Reallocated_Sector_Ct")

                            EE = re.findall(r'(End-to-End_Error(.*))', yp_info[1])
                            if len(EE) != 0:
                                x = EE[0][1].split()[-1]
                                x = int(x)
                                if x == 0:
                                    write_log("End-to-End_Error is OK")
                                else:
                                    write_log(sn[1])
                                    write_log("End-to-End_Error is fail")
                                    self.results['hdd_log'] = 'fail'
                                    self.result_fail()
                            else:
                                write_log("cannot find End-to-End_Error")

                            PH = re.findall(r'(Power_On_Hours(.*))', yp_info[1])
                            if len(PH) != 0:
                                x = PH[0][1].split()[-1]
                                x = int(x)
                                if x < 50000000:
                                    write_log("Power_On_Hours is OK")
                                else:
                                    write_log(sn[1])
                                    write_log("Power_On_Hours is fail")
                                    self.results['hdd_log'] = 'fail'
                                    # result_fail(self)
                                    self.result_fail()
                            else:
                                write_log("cannot find Power_On_Hours")

                            CP = re.findall(r'(Current_Pending_Sector(.*))', yp_info[1])
                            if len(CP) != 0:
                                x = CP[0][1].split()[-1]
                                x = int(x)
                                if x == 0:
                                    write_log("Current_Pending_Sector is OK")
                                else:
                                    write_log(sn[1])
                                    write_log("Current_Pending_Sector is fail")
                                    self.results['hdd_log'] = 'fail'
                                    # result_fail(self)
                                    self.result_fail()
                            else:
                                write_log("cannot find Current_Pending_Sector")
                        else:
                            write_log(sn[1])
                            write_log("SMART overall-health self-assessment test result is fail")
                            self.results['hdd_log'] = 'fail'
                            # result_fail(self)
                            self.result_fail()

            else:
                write_log("cannot find the hdd and ssd,pleace check about")

    def look_ecc(self):
        MCE_ECC(Item).cpu_mce_check()
        MCE_ECC(Item).mem_ecc_check()
        # class MCE_ECC(Item):

    def check_mcelog1(self):
        error_log = []
        match_keys = "above temperature, being removed, CATEER, critical, Corrected, scrub error, degraded, dead device, " \
                     "Device offlined, device_unblocked, error, err,  failed, failure, fault, HDD block removing handle, " \
                     "hard resetting link, IERR, lost, machine check events, MCA, MCE Log, no readable, resetting link, " \
                     "scsi hang, single - bit ECC, soft lockup timeout, Temperature  above threshold, task abort," \
                     "overcurrent, offline device,retry,uncorrect,call_trace, blocked for more than"
        white_list = "qwert,yuiop, XCB error, gssproxy"

        cmd = "cat /var/log/messages"
        msg_info = commands.getstatusoutput(cmd)
        if msg_info[0] == 0:
            for line in msg_info[1].split('\n'):
                pattern = "|".join(match_keys.split(","))
                ignore = "|".join(white_list.split(","))
                if re.search(pattern, line, re.IGNORECASE):
                    if not re.search(ignore, line, re.IGNORECASE):
                        error_log.append(line)
        # write_log(error_log)
        else:
            # write_log(msg_info)
            self.report_info('F')
            self.on_fail("get mce log messages error")
            self.results['mce_log'] = 'fail'
            # result_fail(self)
            self.result_fail()

        if (len(error_log) > 0):
            write_log(error_log)
            write_log("------------ The mce log messages error ------------")
            self.report_info('F')
            self.on_fail("mce log black keys error")
            self.results['mce_log'] = 'fail'
            self.result_fail()
        else:
            write_log("------------ check_mcelog pass ------------")
            

    def check_mcelog(self):
        cmd = "cat /var/log/mcelog"
        mce_log = commands.getstatusoutput(cmd)
        if mce_log[0] == 0:
            if len(mce_log[1]) > 0:
                if "mcelog: mcelog server already running" in mce_log[1]:
                    write_log("------------ check_mcelog pass ------------")
                else:
                    write_log("------------ The mce log messages error ------------")
                    self.report_info('F')
                    self.on_fail("mce log error")
                    self.results['mce_log'] = 'fail'
                    self.result_fail()
            else:
                write_log("------------ check_mcelog pass ------------")
        else:
            write_log("get mce log fail: %s" %mce_log[1])
            self.report_info('F')
            self.on_fail("get mce log messages error")
            self.results['mce_log'] = 'fail'
            self.result_fail()  
                

    def check_PCIE_errors(self):
        dev_AER = {}
        dev_list = []
        cmd = "lspci"
        dev_info = self.run_cmd(cmd).split('\n')
        for dev in dev_info:
            bdf = dev.split()[0]
            dev_list.append(bdf)
        for dev in dev_list:
            cmd = "lspci -s  %s -vvvv" % (dev)
            dev_info = self.run_cmd(cmd).split('\n')
            for num in range(0, len(dev_info)):
                if "Advanced Error Reporting" in dev_info[num]:
                    write_log("check %s AER start" % dev)
                    if "UESta" in dev_info[num + 1]:
                        UESta = dev_info[num + 1]
                    if "UEMsk" in dev_info[num + 2]:
                        UEMsk = dev_info[num + 2]
                    if "CESta" in dev_info[num + 4]:
                        CESta = dev_info[num + 4]
                    if "CEMsk" in dev_info[num + 5]:
                        CEMsk = dev_info[num + 5]

                    for index in range(0, len(UEMsk.split())):
                        if "-" in UEMsk.split()[index]:
                            if "+" in UESta.split()[index]:
                                write_log(UESta)
                                dev_AER[dev + ".UESta"] = UESta
                                self.on_fail(dev)

                    for index in range(0, len(CEMsk.split())):
                        if "-" in CEMsk.split()[index]:
                            if "+" in CESta.split()[index]:
                                write_log(CESta)
                                dev_AER[dev + ".CESta"] = CESta
                                self.on_fail(dev)
                    write_log("check %s AER end" % dev)

        if (len(dev_AER) > 0):
            self.report_info('F')
            self.on_fail()
            write_log("------------ The check PCIE is error ------------")
            self.results['check_AER'] = 'fail'
            self.result_fail()
        else:
            write_log('check PCIE AER Bit normal')

        return

    def check_SEL(self):
        match_keys = "abort,cancel,correctable ECC,critical,degrate,disconnect,Deasserted,down,expired,Err,Error," \
                     "exception,failed,failure,Fault,halt,hot,insufficient,link down,linkdown,limit,lost,miss," \
                     "Mismatch,shutdown,shut down,shortage,unstable,unrecoverable,unreachable," \
                     "Uncorrectable ECC,warning"
        white_list = "qwert,yuiop"
        sel_list = []
        cmd = "ipmitool sel elist"
        sel_info = self.run_cmd(cmd).split('\n')
        for line in sel_info:
            pattern = "|".join(match_keys.split(","))
            ignore = "|".join(white_list.split(","))
            if re.search(pattern, line, re.IGNORECASE):
                if not re.search(ignore, line, re.IGNORECASE):
                    sel_list.append(line)

        if (len(sel_list) > 0):
            write_log(sel_list)
            self.report_info('F')
            write_log("------------ balcklist SEL key error ------------")
            self.on_fail("balcklist SEL key error")
            # self.finished = True
            self.results['check_SEL_ERROR'] = 'fail'
            self.result_fail()
            # ar.pause()

    def check_ethernet_errors(self):
        errors_dev = {}
        result = self.run_cmd('ls -1 /sys/class/net/ |grep -Ev "lo|enx|vir"').split('\n')

        for dev in result:
            cmd = 'ethtool  %s |grep -i "Speed"' % (dev)
            ret_info = self.run_cmd(cmd)
            if 'Mb/s' in ret_info:
                speed = int(ret_info.split()[1].split('Mb/s')[0])
                if speed <= 1000:
                    continue

            err_count = 0
            cmd = 'ethtool -S  %s |grep -iE "err|drop|crc"' % (dev)
            dev_info = self.run_cmd(cmd).split('\n')
            for i in dev_info:
                index = i.rfind(":")
                # index=0
                # key_name = l[:index].strip()
                value = int(i[index + 1:].strip())
                # value=int(l[1].strip())
                err_count += value
                # err_count =0
            '''
            cmd = 'ifconfig %s|grep -iE "err|drop"'%(dev)
            dev_info = self.run_command(cmd,False).get_payload().split('\n')
            for l in dev_info:
                errors_cnt = int(l.strip().split()[2])
                dropped_cnt = int(l.strip().split()[4])
                err_count += errors_cnt
                err_count += dropped_cnt
            '''

            if (err_count != 0):
                errors_dev[dev] = str(err_count)
            write_log("%s network port Bit number: %d" % (dev, err_count))

        if (len(errors_dev) > 0):
            write_log("------------ The check ethernet is error ------------")
            write_log("check network port Bit:" + str(errors_dev))
            self.on_fail("network port Bit")
            self.report_info('F')
            # self.finished = True
            self.results['check_Eth_ERROR'] = 'fail'
            self.result_fail()

    def report_info(self, st):
        # loopinfo = "%s-%s\n" % (self.loop, time.strftime("%H%M%S%Y%m%d", time.localtime()))
        # status = 'Testing\n'
        if st == 'F':
            # status = 'FAIL\n'
            write_log("This test fail")
        if st == 'P':
            # status = 'PASS\n'
            write_log("test pass!")

    def on_fail(self, msg=None):
        # write_log("error")
        # write_log("end of this test")
        self.success = False
        self.finished = True
        # self.show_fail(msg)


def write_log(s):
    with open(c.BLACK_LIST_LOG, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)
