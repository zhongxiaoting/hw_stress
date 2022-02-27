import sys,time
sys.path.append("..")
from main.item import Item

class LOG_CLEAN_TEST(Item):
    def __init__(self,info):
        self.info = info
        print('LOG-CLEAN-TEST')
        
    def run_item(self):
        time.sleep(5)
        self.result_pass()