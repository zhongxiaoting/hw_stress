from utils import log as l
def item_test(func):
    def wrapper(*args, **kw):
        if func(*args, **kw):
            l.log(">> "+ func.__name__ +"test is success!",1,True)
        else:
            l.log(">> "+ func.__name__ +"test is fail!",2,True)
    return wrapper