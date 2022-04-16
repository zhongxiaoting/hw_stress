# coding=utf-8
import commands
import multiprocessing
import os
import re
import time

from main.item import Item
import sys
from common import common_value as cv, constants as c
from utils import decorator
from utils import handle as h

sys.path.append("..")


class MEM_STRESS(Item):
    def __init__(self, info):
        super(MEM_STRESS, self).__init__()
        self.info = info

    # get free memory
    def get_mem(self):
        out = self.run_cmd("free -m|grep Mem")
        mem = out.split()[3]
        # print(mem)
        return int(mem) - 10240

    def mem_check(self, every_mem, i):
        # cv.remove_log(c.MEM_STRESS_LOG_PATH)
        # free_mem = 10240
        # free_mem = self.get_mem() * 0.8
        # self.lock = multiprocessing.Lock()
        shell = "timeout {} taskset -c {} ./tools/memtester {} 1".format(c.RUN_SECONDS, i, every_mem)
        write_log("The Command Line ->>> " + shell + "\n")
        mem_info = commands.getoutput(shell)
        rep = {'\x2d': '', '\x08': '', '\x5c': '', '\x7c': '', '\x2f\x08': ''}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        patternByte = re.compile("|".join(rep.keys()))
        outByte = patternByte.sub(lambda m: rep[re.escape(m.group(0))], mem_info.encode("utf-8"))
        ret = re.sub("\s*setting\s*\d*\s*|\s*testing\s*\d*\s*", "", outByte.decode("utf-8"))
        with self.lock:
            with open(c.MEM_STRESS_LOG_PATH, "at") as f:
                f.write("\n->>NO {} processor: \n".format(i))
                f.write(ret + "\n")

    def run_item(self):
        # judge items is or not run all stress
        args = sys.argv
        if len(args) == 3:
            if int(args[2]) == 1:
                time.sleep(c.WAIT_LAN_TIME)
                for cnt in range(0, 5):
                    time.sleep(30)
                    ret = self.run_cmd("pidof lan_while.sh")
                    if ret:
                        break
                    else:
                        print "waiting lan network run..."

        mem = int(self.get_mem() * 0.8)
        thread_num = cv.get_thread_num()
        every_mem = int(mem / (thread_num - 2))
        write_log("=============  MEM Stress Check Begin  " + get_local_time_string() + " ================")
        self.lock = multiprocessing.Lock()
        l = []
        for i in range(1, thread_num):
            p = multiprocessing.Process(target=self.mem_check, args=(every_mem, i))
            l.append(p)
            p.start()

        for i in l:
            i.join()
        write_log("\n" + "==============  MEM Stress Check End  " + get_local_time_string() + " =================")

        # check memory log
        with open(c.MEM_STRESS_LOG_PATH, "ra+") as f:
            for i in f:
                if "fail" in i or "error" in i:
                    s = "->>>\033[31m MEM Check Fail \033[0m"
                    print s
                    f.write(str(s))
                    f.flush()
                    os.fsync(f)
                    self.stress_fail()
                    return

            s = "->>>\033[32m MEM Check PASS \033[0m "
            print s
            f.write(s)
            f.flush()
            os.fsync(f)
        return


def write_log(s):
    with open(c.MEM_STRESS_LOG_PATH, 'a+') as f:
        print(s)
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def get_local_time_string():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))
