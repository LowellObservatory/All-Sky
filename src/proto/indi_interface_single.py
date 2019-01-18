#!/usr/bin/env python

import sys
import time
import PyIndi
import io
from datetime import datetime
from glob import glob
import os


class IndiClient(PyIndi.BaseClient):
    device = None

    def __init__(self, exptime, datapath, filename):
        super(IndiClient, self).__init__()
        self.exptime = exptime
        self.datapath = datapath 
        self.filename = filename
        self.object   = object

    def newDevice(self, d):
        # if d.getDeviceName() == "SX CCD UltraStar":
        if d.getDeviceName() == "SX CCD SuperStar":
            self.device = d
        else:
            print('You are likely talking to the wrong camera')

    def newProperty(self, p):
        if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
            # connect to device
            self.connectDevice(self.device.getDeviceName())

            # set BLOB mode to BLOB_ALSO
            self.setBLOBMode(1, self.device.getDeviceName(), None)

        if p.getName() == "CCD_EXPOSURE":
            # take first exposure
            self.takeExposure()

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        # get image data
        print('46')
        img = bp.getblobdata()

        # write image data to BytesIO buffer
        blobfile = io.BytesIO(img)
        print('51')

        # open a file and save buffer to disk
        try:
            with open(self.datapath + self.filename, "wb") as f:
                print('56')
                f.write(blobfile.getvalue())
                print('58')
        except OSError as e:
            print('60')
            print('error: ' + str(e))
                

        # start new exposure
        self.takeExposure()
        print('66')

    def newSwitch(self, svp):
        print('69')
        # pass

    def newNumber(self, nvp):
        print('73')
        # pass

    def newText(self, tvp):
        print('77')
        # pass

    def newLight(self, lvp):
        print('81')
        # pass

    def newMessage(self, d, m):
        print('85')
        # pass

    def serverConnected(self):
        print('89')
        print("Server connected (" + self.getHost() + ":" + str(self.getPort()) + ")")
        print('91')

    def serverDisconnected(self, code):
        print('94')
       #  pass

    def takeExposure(self):
        # get current exposure time
        print('99')
        exp = self.device.getNumber("CCD_EXPOSURE")
        print('101')

        # set exposure time to 5 seconds
        exp[0].value = float(self.exptime)

        # send new exposure time to server/device
        self.sendNewNumber(exp)
