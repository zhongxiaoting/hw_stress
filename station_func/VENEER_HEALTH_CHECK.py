import utils.log
from main.item import Item
from utils import log as l


CMD_GET_VENEER = 'dmesg | grep -i warn'


class VENEER_HEALTH_CHECK(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.veneer_check()


    def veneer_check(self):
        veneer_infor = self.run_cmd(CMD_GET_VENEER)
        l.write_debug_log(veneer_infor)
        l.log(veneer_infor)

