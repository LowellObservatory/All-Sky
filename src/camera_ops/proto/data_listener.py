
import stomp
import threading
import time as tm
import os
import numpy as np
import sys
from protoLOFITS import FitsOps    


class ConnectionListener(object):
    def __init__(self):
        self.server = ''
        self.port = 61613
        self.dest = '/topic/test_img'
        self.conn = stomp.Connection([(self.server, self.port)])
        self.conn.set_listener('', self)
        self.conn.start()
        self.conn.connect()
        self.conn.subscribe(destination=self.dest, id='data_xfer', ack='auto')

    @staticmethod
    def on_error(headers, message):
        sys.stderr.write("received an error: {}\n".format(headers))
        sys.stderr.write("received an error: {}\n".format(message))

    @staticmethod
    def on_message(headers, message):
        fo.environmental()
        fo.sun_moon()
        fo.fits_header(message)


acq = ConnectionListener()
fo = FitsOps()

while True:
    tm.sleep(1)
