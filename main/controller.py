# coding=utf-8
import sys
from do import do
sys.path.append("..")
from common import constants as c
from utils import handle as h, log as l


class Controller(object):

    def __init__(self):
        self.cfg = h.read_cfg(c.CFG_PATH)
        self.ctrl = h.read_cfg(c.CONTROLLER_JSON_PATH)

    # test control
    def start_helper(self,index = 0, item_index = 0):
        if not self.backup(index, item_index):
            return
        if int(index) == 0 and int(item_index) == 0:
            self.start_all()
        elif int(index) != 0 and int(item_index) == 0:
            self.start_station(index)
        else:
            self.start_item(index,item_index)
 
    # 1. define entire test 
    def start_all(self):
        if not self.ctrl['KEEP_TEST']:
            self.input_info()
            self.update_ctrl(1,1,False)
        for index in range(self.ctrl['INDEX'] - 1,len(self.cfg)):
            station = self.cfg[index]
            self.update_ctrl(station['index'],1)
            if not self.ctrl['KEEP_TEST']:
                if index > 0 and index < len(self.cfg):
                    l.title_station_pass(self.cfg[index -1]['name'])
                l.title_station(self.cfg[index]['name'])
            for i in range(self.ctrl['ITEM_INDEX'] - 1,len(self.cfg[index]['items'])):
                item = self.cfg[index]['items'][i]
                if item['switch'] == 'off':
                    continue
                if not self.ctrl['KEEP_TEST']:
                    l.title_item(item['name'])
                self.update_ctrl(station['index'],item['item_index'],item['keep_test'])
                do(station['name'],item)
        l.title_station_pass(self.cfg[-1]['name'])

    # 2. define work station test
    def start_station(self,index):
        for station in self.cfg:
            if station['index'] == int(index):
                l.title_station(station['name'])
                for item in station['items']:
                    if item['switch'] == 'off':
                        continue
                    l.title_item(item['name'])
                    do(station['name'],item)
                    
    # 3. define single test for debug
    def start_item(self,index, item_index):
        for station in self.cfg:
            if station['index'] == int(index):
                l.title_station(station['name'])
                for item in station['items']:
                    if item['item_index'] == int(item_index):
                        l.title_item(item['name'])
                        do(station['name'], item)


    # copy last result.log to log_backup folder
    def backup(self, index, item_index):
        if int(index) == 0 and int(item_index) == 0 :
            return True
        if int(index) > 0 and int(item_index) == 0 and int(index)<=len(self.cfg):
            return True
        if int(index) > 0 and int(index)<=len(self.cfg):
            if int(item_index) >0 and  int(item_index) <= len(self.cfg[int(index) - 1]['items']):
                return True
            else:
                l.fail_msg("station "+str(index)+" item "+ str(item_index)+" out of range, Please check!")
                return False                         
        else:
            l.fail_msg("station index out of range, Please check!")
            return False 
    
    # wait input info
    def input_info(self):
        self.ctrl['SN'] = h.scan_sn()
        self.ctrl['OPERATOR'] = h.operator()
        h.update_controller_json(self.ctrl)

    # update controller.json info 
    def update_ctrl(self,index,item_index,keep_test = False):
        self.ctrl['INDEX'] = index
        self.ctrl['ITEM_INDEX'] = item_index
        self.ctrl['KEEP_TEST'] = keep_test
        h.update_controller_json(self.ctrl)

     # if test fail will stop the project
    @staticmethod
    def pasue():
        l.fail_msg("Test Fail, Please check progress!")
        sys.exit(1)