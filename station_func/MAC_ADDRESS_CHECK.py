import re

import utils.log
from main.item import Item
from utils import log as l
from utils import decorator

CMD_GET_MAC = 'ifconfig'
class MAC_ADDRESS_CHECK(Item):
    def __init__(self, info):
        self.info = info

    def run_item(self):
        self.mac_check()


    def mac_check(self):
        mac_address = self.run_cmd(CMD_GET_MAC)
        l.write_debug_log(mac_address)
        mac_infor = re.findall(r'(ether (.*))', mac_address)
        print(mac_infor)



