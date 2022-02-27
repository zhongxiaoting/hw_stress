import sys,time
sys.path.append("..")
from main.item import Item

class HOST_CFG_SET(Item):
    def __init__(self,info):
        self.info = info
        print('HOST-CFG-SET')
        
    def run_item(self):
        time.sleep(5)
        self.result_pass()