from utils import log as l


def item_test(func):
    def wrapper(*args, **kw):
        if "Fail" in func(*args, **kw):
            l.fail_msg(">> " + func.__name__ + " test is fail!" + "\n")
        else:
            l.pass_msg(">> " + func.__name__ + " test is success!" + "\n")

    return wrapper
