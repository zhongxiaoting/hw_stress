# coding=utf-8
import sys
sys.path.append("..")
import requests as r
from utils import log as l,handle as h
from common import constants as c
import controller as ctrl
import commands

class Item(object):

    def __init__(self):
        # self.t_pass = Fail
        self.result_json = {}
        # self.info = {}
        

    def run(self):
        self.run_item()
        return

    # child class must implement the method
    def run_item(self):
        raise NotImplementedError

    # write result our need show info 
    def set_json(self,k,v):
        self.result_json[k] = v

    # check mes status
    def check_mes_connect(self):
        response =r.Request().get(c.MES_HOST)
        if response:
            print(response)

    # test pass
    def result_pass(self):
        l.title_item('PASS ')
        
    # test fail
    def result_fail(self):
        l.fail_msg('Fail')
        ctrl.Controller.pasue()
        return 

    # cmd check
    def run_cmd(self, cmd):
        data =h.run_cmd(cmd)
        if data:
            return data
        return data

    # stress fail
    def stress_fail(self):
        l.fail_msg("Test Fail, Please check progress!")
        h.run_cmd("pkill -9 python")
        h.run_cmd("pkill -9 stress")
        h.run_cmd("pkill -9 memtester")
        h.run_cmd("pkill -9 fio")
        h.run_cmd("pkill -9 lan_while.sh")
        sys.exit(1)
        return

    # formal quit
    def lan_formal_quit(self):
        self.run_cmd("pkill -9 lan_while.sh")
        sys.exit(0)
        return


