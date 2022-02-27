# coding=utf-8
import commands
import os
import re
import sys
from main.item import Item
from utils import decorator, log as l
from common import common_value
import time
sys.path.append("..")

class ItemBlacklistCheck(Item):

    def __init__(self,info):
        super(ItemBlacklistCheck, self).__init__()
        self.info=info
        self.finished = False
        self.results = {}

    def run_item(self):
        self.report_info('S')
        self.check_hdd()
        #self.check_mcelog()
        #self.check_ethernet_errors()
        #self.check_PCIE_errors()
        #self.check_SEL()
        l.log('check blacklist finished')
        if len(self.results) == 0:
            self.report_info('P')
            #self.on_pass()
            l.log("ALL GOOD")
        else:
            self.report_info('F')
            l.log(self.results, False)
            self.on_fail()
        self.finished = True


    def check_hdd(self):
        panfu_list=[]
        yingpan_list=[]
        yp_info = []
        cmd='/opt/MegaRAID/MegaCli/MegaCli64 -LdPdInfo -aALL | grep "Device Id:"'

        hdd_number=self.run_cmd(cmd).split('\n')
        cmd='ls /sys/class/block |grep -Ev "loop*|ram*|nvme|dm"'
        hdd_name=self.run_cmd(cmd).split('\n')

        for i in hdd_number:
            panfu=i.split()[2]
            panfu_list.append(panfu)
            print(panfu_list)
        #much=len(panfu_list)

        for i in hdd_name:
            yingpan=i.split()[0]
            yingpan_list.append(yingpan)

    #for num in range(0, len(dev_info)):


        for i in range(0,len(panfu_list)):
            cmd = 'smartctl -a -d megaraid,%s /dev/%s ' % (panfu_list[i],yingpan_list[i])
            #print('smartctl -a -d megaraid,' %s /dev/ %s ',%) 
            print(cmd)
            yp_info=self.run_cmd(cmd).split('\n')
            for i in yp_info:
                if "SMART overall-health self-assessment test result: PASSED" in i:
                    print("smart go")
                    l.log("it is time to check hdd_info: SMART overall-health self-assessment test result: PASSED")
            yp_info=str(yp_info)
            one = re.findall(r'((.*)Reallocated_Sector_Ct(.*))',yp_info)
            print(one)



    def check_mcelog(self):
        error_log = []
        match_keys = "above temperature, being removed, CATEER, critical, Corrected, scrub error, degraded, dead device, " \
                     "Device offlined, device_unblocked, error, err,  failed, failure, fault, HDD block removing handle, " \
                     "hard resetting link, IERR, lost, machine check events, MCA, MCE Log, no readable, resetting link, " \
                     "scsi hang, single - bit ECC, soft lockup timeout, Temperature  above threshold, task abort," \
                     "overcurrent, offline device,retry,uncorrect,call_trace, blocked for more than"
        white_list = "qwert,yuiop"
        white_list = "qwert,yuiop, XCB error, gssproxy"
        cmd = "dmesg"
        dmsg_info = self.run_cmd(cmd).split('\n')
        for line in dmsg_info:
            pattern = "|".join(match_keys.split(","))
            ignore = "|".join(white_list.split(","))
            if re.search(pattern, line, re.IGNORECASE):
                if not re.search(ignore, line, re.IGNORECASE):
                    error_log.append(line)

        l.log(error_log)
        cmd = "cat /var/log/messages"
        msg_info = commands.getstatusoutput(cmd)
        if msg_info[0] == 0:
            for line in msg_info[1].split('\n'):
                pattern = "|".join(match_keys.split(","))
                ignore = "|".join(white_list.split(","))
                if re.search(pattern, line, re.IGNORECASE):
                    if not re.search(ignore, line, re.IGNORECASE):
                        error_log.append(line)
        else:
            self.report_info('F')
            self.on_fail("get os log messages error")
            self.results['os_log'] = 'fail'


        if (len(error_log) > 0):
            l.log(error_log)
            self.report_info('F')
            self.on_fail("OS log black keys error")
            self.results['os_log'] = 'fail'


        #hdd_keys="SMART overall-health self-assessment test result: PASSED"\




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
                    l.log("check %s AER start" % dev, False)
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
                                l.log(UESta)
                                dev_AER[dev + ".UESta"] = UESta
                                self.on_fail(dev)

                    for index in range(0, len(CEMsk.split())):
                        if "-" in CEMsk.split()[index]:
                            if "+" in CESta.split()[index]:
                                l.log(CESta)
                                dev_AER[dev + ".CESta"] = CESta
                                self.on_fail(dev)
                    l.log("check %s AER end" % dev, False)

        if (len(dev_AER) > 0):
            self.report_info('F')
            self.on_fail()
            self.results['check_AER'] = 'fail'
        else:
            l.log('check PCIE AER Bit normal')

        return


    def check_SEL(self):
        match_keys = "abort,cancel,correctable ECC,critical,degrate,disconnect,Deasserted,down,expired,Err,Error," \
                     "exception,failed,failure,Fault,halt,hot,insufficient,link down,linkdown,limit,lost,miss," \
                     "Mismatch,reset,shutdown,shut down,shortage,unstable,unrecoverable,unreachable," \
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
            l.log(sel_list)
            self.report_info('F')
            self.on_fail("balcklist SEL key error")
            #self.finished = True
            self.results['check_SEL_ERROR'] = 'fail'
            #ar.pause()




    def check_ethernet_errors(self):
        errors_dev = {}
        result = self.run_cmd('ls -1 /sys/class/net/ |grep -Ev "lo|enx"').split('\n')

        for dev in result:
            cmd = "ethtool  %s |grep Speed"%(dev)
            ret_info = self.run_cmd(cmd)
            if 'Mb/s' in ret_info:
                speed = int(ret_info.split()[1].split('Mb/s')[0])
                if speed <= 1000:
                    continue

            err_count = 0
            cmd = 'ethtool -S  %s |grep -iE "err|drop|crc"'%(dev)
            dev_info = self.run_cmd(cmd).split('\n')
            for i in dev_info:
                index = i.rfind(":")
                #index=0
                #key_name = l[:index].strip()
                value = int(i[index+1:].strip())
                #value=int(l[1].strip())
                err_count += value
                #err_count =0
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
            l.log("%s network port Bit number: %d" %(dev, err_count))

        if ( len(errors_dev) > 0 ):
            l.log("check network port Bit:" + str(errors_dev))
            self.on_fail("network port Bit")
            self.report_info('F')
            #self.finished = True
            self.results['check_Eth_ERROR'] = 'fail'


    def report_info(self,st):
        #loopinfo = "%s-%s\n" % (self.loop, time.strftime("%H%M%S%Y%m%d", time.localtime()))
        #status = 'Testing\n'
        if st == 'F':
            #status = 'FAIL\n'
            l.log("This test fail")
        if st == 'P':
            #status = 'PASS\n'
            l.log("test pass!")

    def on_fail(self,msg=None):
        #l.log("error")
        #l.log("end of this test")
        self.success = False
        self.finished = True
        self.show_fail(msg)



















