import sys,json
import requests as r,handle
sys.path.append("..")
from common import constants as c


# get hardware configure
def get_hw_cfg():
    res = r.get(c.UPLOAD_HW_CFG).json()
    if not res:
        return False
    f = open(c.LOCAL_HW_CFG,'w')
    json.dump(res,f)
    f.close()
    return True

def upload_hw_cfg():
    hw_cfg = handle.read_cfg(c.LOCAL_HW_CFG)
    print(hw_cfg)
    res = r.post(c.UPLOAD_HW_CFG,hw_cfg)
    print(res)
