# coding=utf-8
import sys,time, re,datetime

sys.path.append("..")
from main.item import Item
from utils import log as l,decorator
###############
#  Constants
###############
CONST_SLEEP_TIME = 6 # sleep time


###############
# Command
###############

CMD_GET_NOW_TIME = 'cat /proc/driver/rtc'  # 获得目前时间
CMD_CLOSE_TIME_SYNC = 'timedatectl set-ntp no' # 关闭时间同步

class RTC_CHECK(Item):
    def __init__(self,info):
        self.info = info
        
    def run_item(self):
        self.set_datetime()
        self.precision_check()
        self.result_pass()
        
       
    @decorator.item_test
    def precision_check(self):
        t1 = self.run_cmd(CMD_GET_NOW_TIME)
        l.log(str(t1))
        time.sleep(CONST_SLEEP_TIME)
        t2 = self.run_cmd(CMD_GET_NOW_TIME)
        l.log(str(t2))
        diff_s =self.compose_time(self.get_rtc_date_time(t2)) - self.compose_time(self.get_rtc_date_time(t1))
        if diff_s <= CONST_SLEEP_TIME + 1:
            return True
        else:
            return False
        
        

    def get_rtc_date_time(self, payload):
        temp = payload.split('\n')
        rtc_time = None
        rtc_date = None
        for s in temp:
            if re.match('rtc_time', s):
                rtc_time = "".join(s.split(" ")[1]).lstrip()
            elif re.match('rtc_date', s):
                rtc_date = s.split(":")[1].lstrip()
            else:
                continue
        return rtc_date + ' ' + rtc_time

    def compose_time(self, str):
        time2 = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        time3 = time.mktime(time2.timetuple())
        return int(time3)

    @decorator.item_test
    def set_datetime(self):
        r = self.run_cmd(CMD_CLOSE_TIME_SYNC)
        return r
           
        

    