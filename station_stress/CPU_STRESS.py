# coding=utf-8
import os
import sys
import threading
import time

from main.item import Item
from utils import decorator
from common import common_value as cv, constants as c

sys.path.append("..")


class CPU_STRESS(Item):
    def __init__(self, info):
        super(CPU_STRESS, self).__init__()
        self.info = info

    def run_item(self):
        args = sys.argv
        if len(args) == 3:
            if int(args[2]) == 1:
                time.sleep(c.WAIT_LAN_TIME + 20)
                for cnt in range(0, 5):
                    time.sleep(30)
                    ret = self.run_cmd("pidof lan_while.sh")
                    if ret:
                        break
                    else:
                        print "waiting lan network run..."
        self.stress_check()

    def top_log(self):
        maxTimes = c.RUN_SECONDS / 10
        self.run_cmd("setsid timeout {} top -d 10 -n {} -b -i >> {}".format(c.RUN_SECONDS, maxTimes, c.STRESS_LOG))

    @decorator.item_test
    def stress_check(self):
        thread_num = cv.get_thread_num()
        # cv.remove_log(c.CPU_STRESS_LOG_PATH)
        shell = "./tools/stress -c {} -t {} ".format(thread_num, c.RUN_SECONDS)
        # print(cpu_infor)
        write_log("=============  CPU Stress Check Begin  " + get_local_time_string() + " ================")
        write_log("The Command Line ->>> " + shell + "\n")
        cpu_infor = os.popen(shell)
        t = threading.Thread(target=self.top_log)
        t.setDaemon(True)
        t.start()
        out = cpu_infor.read()
        write_log(out)
        write_log("==============  CPU Stress Check End  " + get_local_time_string() + " =================")
        # check errors
        if "successful run completed" in out:
            write_log("->>>\033[32m CPU Check PASS \033[0m ")
        else:
            write_log("->>>\033[31m CPU Check Fail \033[0m")
            self.stress_fail()
        return out


def write_log(s):
    with open(c.CPU_STRESS_LOG_PATH, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))
