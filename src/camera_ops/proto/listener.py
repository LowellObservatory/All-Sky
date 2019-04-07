
import stomp
import time as tm
import os
import sys
from astropy.io import fits
from astropy.io.fits import ImageHDU
import base64


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

    def on_message(self, headers, message):
        print(headers)

        imgdata = ImageHDU.fromstring(base64.b64decode(message))
        fits.writeto('testfits.fits', imgdata.data, imgdata.header, overwrite=True)

        statvar = False
        self.breakout(statvar)

    @staticmethod
    def breakout(statvar):
        if statvar is False:
            os._exit(0)


acq = ConnectionListener()
acq.breakout(True)

while True:
    tm.sleep(1)
