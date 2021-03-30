import time
from coilcalc._settings import DEV


class Logger(object):
    def __init__(self):
        self.tzero = dict()

    def clear_timer(self, keyid):
        self.tzero[keyid] = time.time()

    def timestamp(self, keyid, message="Unspecified event"):
        if DEV:
            print("%s : %.3f" % (message, time.time() - self.tzero[keyid]))

    def log_event(self, message):
        print(message)


logger = Logger()
