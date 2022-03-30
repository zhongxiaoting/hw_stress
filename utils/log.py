# coding=utf-8
import sys, os, time
import times as t

sys.path.append("..")
from common import constants as c


###############
# 1. print
###############

# define print pass info
def pass_msg(s):
    print("\033[32m" + s + "\033[0m")


# define print fail info
def fail_msg(s):
    print("\033[31m" + s + "\033[0m")


# define print msg info
def msg(s):
    print(s)


# # define print pass logo
# def pass_logo():
#     for line in logo.PASS_LOGO:
#         print("\033[32m" + line + "\033[0m")
#
#
# # define print fail logo
# def fail_logo():
#     for line in logo.FAIL_LOGO:
#         print("\033[31m" + line + "\033[0m")


###############
#  2. file 
###############

# write log
def write_log(s):
    with open(c.FULL_LOG_PATH, 'a+') as (f):
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


def write_debug_log(s):
    with open(c.FULL_LOG_PATH, 'a+') as (f):
        f.write(str(s) + '\n')
        f.flush()
        os.fsync(f)


# define log write reulst.log
def log(s, m_type=0, w=False):
    if not s:
        return
    if m_type == 1:
        w = True
        pass_msg(s)
    elif m_type == 2:
        fail_msg(s)
    else:
        msg(s)
    # if w:
        # write_log(s)
    # write_debug_log(s)
    write_log(s)


# get local_time
def local_time():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# define station title
def title_station(title):
    print "==================================="
    print title + ' ' + t.local_time()
    print "==================================="


# define station title pass
def title_station_pass(title):
    log("===============================================", 1)
    log(title + ' PASS ' + t.local_time(), 1)
    log("===============================================\n", 1)


# define item title
def title_item(title):
    print "======== " + title + ' ' + t.local_time() + "========\n"


# # backup log
# def backup_log():
#     # backup result.log
#     if os.path.exists(c.RESULT_LOG_PATH):
#         os.rename(c.RESULT_LOG_PATH, c.LOG_BACKUP_DIR + '/result/' + t.local_time() + '.log')
#     if os.path.exists(c.FULL_LOG_PATH):
#         os.rename(c.FULL_LOG_PATH, c.LOG_BACKUP_DIR + '/full/' + t.local_time() + '.log')
