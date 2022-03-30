# coding=utf-8
from common import make_log_dir as m
sn_path = m.make_sn_dir()
date_log_path = m.make_date_log_dir()

###############
# 1. dir and path
###############
# define test root path
TEST_DIR = '/home/hw_stress'
LOG_PATH = TEST_DIR + '/log/'
STRESS_LOG = LOG_PATH + sn_path + '/' + date_log_path
LOG_BACKUP_DIR = TEST_DIR + '/log'
CFG_PATH = TEST_DIR + '/config/cfg.json'
RESULT_LOG_PATH = TEST_DIR + '/result.log'
FULL_LOG_PATH = TEST_DIR + '/full.log'
CONTROLLER_JSON_PATH = TEST_DIR + '/config/controller.json'
CPU_STRESS_LOG_PATH = STRESS_LOG + '/cpu_stress.log'
MEM_STRESS_LOG_PATH = STRESS_LOG + '/mem_stress.log'
HDD_STRESS_LOG_PATH = STRESS_LOG + '/'
LAN_STRESS_LOG_PATH = STRESS_LOG + '/lan_stress.log'
MCE_ECC_LOG = STRESS_LOG + '/mce_ecc.log'
LOSS_DISK_LOG_PATH = STRESS_LOG + '/loss_disk.log'
STRESS_ALL_LOG = STRESS_LOG + '/' + sn_path + '.log'
BLACK_LIST_LOG = STRESS_LOG + '/blacklistall.log'

###############
# 2. variable
###############

# define operator number minimum value
OPERATOR_MINI_NUMBER = 4

# define run time
RUN_SECONDS = 86400

# loss Disk check wait time
WAIT_LOSS_DISK_TIME = 600

# define loss disk run interval time
LOSS_DISK_TIME = 3600

# wait network run time
WAIT_LAN_TIME = 60

# wait network speed check time
WAIT_LAN_SPEED_TIME = 30

# wait check stress log time
CHECK_STRESS_TIME = 600

# define run file name
CPU_STRESS = "CPU_STRESS"

MEM_STRESS = "MEM_STRESS"

HDD_STRESS = "HDD_STRESS"

LAN_STRESS = "LAN_STRESS"

LOSS_DISK = "LOSS_DISK"

STRESS_ALL = "STRESS_ALL"

###############
# 3. network
###############
# MES host url and port
# MES_HOST = 'http://localhost:3000'

# state = 1 is normal state
STATE_OK = 1

# get hardware info path
# HW_CFG = MES_HOST + '/public/hw_cfg.json'

# upload hardware info path
# UPLOAD_HW_CFG = MES_HOST + '/hw_cfg'

# upload hardware info local path
LOCAL_HW_CFG = TEST_DIR + '/config/hw_cfg.json'

# upload hardware info url
# UPLOAD_HW_CFG = MES_HOST + '/hw_cfg'

# request headers
REQUEST_HEADERS = {"Content-Type": "application/json\; charset=utf-8", "x-request-datasource": "001"}



