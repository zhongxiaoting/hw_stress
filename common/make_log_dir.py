# coding=utf-8
import commands
import os
import time

# define sn  number minimum value
SN_MINI_NUMBER = 6


# scan sn number
def scan_sn():
    sn = ''
    while True:
        sn = raw_input('Please scan SN number:')
        if len(sn) < SN_MINI_NUMBER:
            print("SN number too short, Please retry!")
            continue
        else:
            print("Scan sn is: " + sn)
            break
    return sn


sn_path = scan_sn()


# make an SN folder to save logs
def make_sn_dir():
    if not os.path.exists('/home/hw_stress/log/' + sn_path):
        make_dir = commands.getstatusoutput('cd log && mkdir %s' % (sn_path))
        return sn_path
    return sn_path


def get_local_time_string():
    return time.strftime('%04Y%m%d%H%M%S', time.localtime(time.time()))


# save logs for each run
def make_date_log_dir():
    make_sn_dir()
    date_dir = str(get_local_time_string())
    if not os.path.exists('/home/hw_stress/log/' + sn_path + '/' + date_dir):
        make_date_dir = commands.getstatusoutput("cd /home/hw_stress/log/%s && mkdir %s" % (sn_path, date_dir))
        return date_dir
    return date_dir


# waiting input run seconds
# author: Hanyuan Chen
def set_run_seconds():
    while True:
        input_run_seconds = raw_input('Please set run seconds:')
        if len(input_run_seconds) == 0 or input_run_seconds.isdigit() == False:
            print "Your input is invalid, Please retry..."
            continue
        else:
            run_seconds = int(input_run_seconds)
            break
    return run_seconds
