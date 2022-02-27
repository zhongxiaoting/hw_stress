import time
# get local_time
def local_time():
    return time.strftime('%04Y-%m-%d %H:%M:%S', time.localtime(time.time())) 