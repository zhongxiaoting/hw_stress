# coding=utf-8
import commands
import multiprocessing
import os
import re
import signal
import time
import subprocess
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
        self.l = []

    # get free memory
    def get_mem(self):
        out = self.run_cmd("free -m|grep Mem")
        mem = out.split()[3]
        # print(mem)
        return int(mem) - 10240

    def mem_check(self):
        # cv.remove_log(c.MEM_STRESS_LOG_PATH)
        # free_mem = 10240
        # free_mem = self.get_mem() * 0.8
        # self.lock = multiprocessing.Lock()

        for i in range(3, 5):
            cmd = "timeout {} taskset -c {} memtester {} 1".format(c.RUN_SECONDS, i, 50)
            write_log("The Command Line ->>> " + cmd + "\n")
            mem_info = subprocess.Popen(cmd, preexec_fn=os.setsid, shell=True, stdout=subprocess.PIPE)
            self.l.append(mem_info)
            # write_log(mem_info.stdout.read())
            # rep = {'\x2d': '', '\x08': '', '\x5c': '', '\x7c': '', '\x2f\x08': ''}
            # rep = dict((re.escape(k), v) for k, v in rep.items())
            # patternByte = re.compile("|".join(rep.keys()))
            # outByte = patternByte.sub(lambda m: rep[re.escape(m.group(0))], mem_info.encode("utf-8"))
            # ret = re.sub("\s*setting\s*\d*\s*|\s*testing\s*\d*\s*", "", outByte.decode("utf-8"))
            # self.lock = os.getpgid(mem_info.pid)
            # with self.lock:
            #     with open(c.MEM_STRESS_LOG_PATH, "at") as f:
            #         f.write("\n->>NO {} processor: \n".format(i))
            #         f.write(ret + "\n")
        return self.l

    # 接收到触发 杀死进程组
    def signal_handler(self, signal, frame):
        print("end")
        for j in self.l:
            os.killpg(os.getpgid(j.pid), 9)

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
        self.mem_check()
        # 接受ctrl c终止信号
        signal.signal(signal.SIGINT, self.signal_handler)
        # 阻塞等待子进程结束
        for k in self.l:
            k.wait()
            """
            mem_info = k.stdout.read()
            rep = {'\x2d': '', '\x08': '', '\x5c': '', '\x7c': '', '\x2f\x08': ''}
            rep = dict((re.escape(k), v) for k, v in rep.items())
            patternByte = re.compile("|".join(rep.keys()))
            outByte = patternByte.sub(lambda m: rep[re.escape(m.group(0))], mem_info.encode("utf-8"))
            ret = re.sub("\s*setting\s*\d*\s*|\s*testing\s*\d*\s*", "", outByte.decode("utf-8"))
            write_log(mem_info)
            """
        print ('finish')

        # mem = int(self.get_mem() * 0.8)
        # thread_num = cv.get_thread_num()
        # every_mem = int(mem / (thread_num - 2))
        # write_log("=============  MEM Stress Check Begin  " + get_local_time_string() + " ================")
        # self.lock = multiprocessing.Lock()
        # l = []
        # for i in range(1, thread_num):
        #     p = multiprocessing.Process(target=self.mem_check, args=(every_mem, i))
        #     l.append(p)
        #     p.start()
        #
        # for i in l:
        #     i.join()
        # write_log("\n" + "==============  MEM Stress Check End  " + get_local_time_string() + " =================")

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
