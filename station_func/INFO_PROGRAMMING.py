import sys,time
sys.path.append("..")
from main.item import Item

class INFO_PROGRAMMING(Item):
    def __init__(self,info):
        self.info = info
        print('INFO-PROGRAMMING')
        
    def run_item(self):
        time.sleep(5)
        self.result_pass()