#!/home/sel/anaconda3/bin/python

import PyIndi
import time
import sys
import threading
import time
from stomp import * 
from datetime import datetime
from glob import glob
from pathlib import Path
import os
from set_frame_type import FrameType

basedir = str(Path.home()) + '/'
utdate = datetime.utcnow().strftime('%Y%m%d')
path = basedir + utdate

if not os.path.exists(path):
    try:
        os.makedirs(path)
    except OSError as e:
        print('Error: ' + str(e))
elif os.path.exists(path):
    os.utime(path, None)

t1 = time.time()


class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.blobEvent = ()
        self.seqno = '0001'
        self.ccd_exposure = 0
        self.ccd = "SX CCD SuperStar"
        device_ccd = self.getDevice(self.ccd)

        if not self.connectServer():
            print("No indiserver running on " + self.getHost() + ":" + str(self.getPort()))
            # Rather than exit attempt to start indi server
            sys.exit(1)

        while not device_ccd:
            time.sleep(0.5)
            device_ccd = self.getDevice(self.ccd)

        ccd_connect = device_ccd.getSwitch("CONNECTION")

        while not ccd_connect:
            time.sleep(0.5)
            ccd_connect = device_ccd.getSwitch("CONNECTION")
        if not (device_ccd.isConnected()):
            ccd_connect[0].s = PyIndi.ISS_ON  # the "CONNECT" switch
            ccd_connect[1].s = PyIndi.ISS_OFF  # the "DISCONNECT" switch
            self.sendNewSwitch(ccd_connect)

        self.device_ccd = device_ccd

    def newDevice(self, d):
        pass

    def newProperty(self, p):
        pass

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        self.blobEvent.set()
        pass

    def newSwitch(self, svp):
        pass

    def newNumber(self, nvp):
        pass

    def newText(self, tvp):
        pass

    def newLight(self, lvp):
        pass

    def newMessage(self, d, m):
        pass

    def serverConnected(self):
        pass

    def serverDisconnected(self, code):
        pass

    def capture(self, nexp, exptime, delay):
        self.ccd_exposure = self.device_ccd.getNumber("CCD_EXPOSURE")

        while not self.ccd_exposure:
            time.sleep(0.5)
            self.ccd_exposure = self.device_ccd.getNumber("CCD_EXPOSURE")

        # we should inform the indi server that we want to receive the
        # "CCD1" blob from this device
        indiclient.setBLOBMode(PyIndi.B_ALSO, self.ccd, "CCD1")
        ccd_ccd1 = self.device_ccd.getBLOB("CCD1")

        while not ccd_ccd1:
            time.sleep(0.5)
            ccd_ccd1 = self.device_ccd.getBLOB("CCD1")

        # a list of our exposure times
        exposures = [exptime] * nexp
 
        # we use here the threading.Event facility of Python
        # we define an event for newBlob event
        i = 0
        self.blobEvent = threading.Event()
        self.blobEvent.clear()
        self.ccd_exposure[0].value = exposures[i]
        self.sendNewNumber(self.ccd_exposure)
        ndelay = exptime + delay
        time.sleep(ndelay)
        self.blobEvent.wait()

        while i < len(exposures):
            if i + 1 < len(exposures):
                self.blobEvent.wait()
                self.ccd_exposure[0].value = exposures[i]
                self.sendNewNumber(self.ccd_exposure)

            for blob in ccd_ccd1:
                print("name: ", blob.name, " size: ", blob.size, " format: ", blob.format)
                fitsdata = blob.getblobdata()

                try:
                    lastimg = sorted(glob(path + '/' + utdate + '_*.fits'))[-1][-9:-5]
                    seq = int(lastimg) + 1
                    self.seqno = '%04d' % seq
                    filename = path + '/' + datetime.utcnow().strftime('%Y%m%d') + '_' + str(self.seqno) + '.fits'
                except IndexError:
                    lastimg = datetime.utcnow().strftime('%Y%m%d') + '_0001.fits'
                    filename = path + '/' + lastimg

                if 0 < i <= len(exposures):
                    ndelay = exptime + delay

                print(filename)

                f = open(filename, 'wb')
                f.write(fitsdata)
                f.close()

            if i + 1 == len(exposures):
                time.sleep(1)
            else:
                time.sleep(ndelay)

            i += 1


if __name__ == '__main__':
    indiclient = IndiClient()
    indiclient.setServer("localhost", 7624)

    ft = FrameType()

    def input_params():
        frame_type = sys.argv[1]
        nexp = int(sys.argv[2])
        exptime = float(sys.argv[3])
        delay = float(sys.argv[4])

        ft.send_new_frame_type(frame_type)
        time.sleep(1.0)
        indiclient.capture(nexp, exptime, delay)

    input_params()

t2 = time.time()
tdiff = t2 - t1
print(f'time to execute: {tdiff:3.2f} secs.')
