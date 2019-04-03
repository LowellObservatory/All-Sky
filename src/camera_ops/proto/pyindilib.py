import PyIndi
import time
import sys
import os
from subprocess import Popen, PIPE

class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.setServer("localhost", 7624)

        ispid = Popen(['/bin/sh', '-c', 'pgrep indiserver'], stdout=PIPE)
        pidis = ispid.communicate()[0].decode()
        if not pidis:
            print('The indiserver is not running. Will attempt to start now...')
            try:
                os.mkfifo('/tmp/indififo')
                Popen(['/bin/sh', '-c', '/usr/bin/indiserver -f /tmp/indififo indi_sx_ccd'], stdout=PIPE)
            except FileExistsError:
                Popen(['/bin/sh', '-c', '/usr/bin/indiserver -f /tmp/indififo indi_sx_ccd'], stdout=PIPE)
            except OSError:
                Popen(['/bin/sh', '-c', '/usr/bin/indiserver indi_sx_ccd'], stdout=PIPE)

        time.sleep(1)

        if not self.connectServer():
            print("No indiserver running on " + self.getHost() + ":" + str(self.getPort()) + " - Try to run")
            sys.exit(1)


        ccd = "SX CCD SuperStar"
        self.device_ccd = self.getDevice(ccd)

        while not(self.device_ccd):
            time.sleep(0.5)
            self.device_ccd = self.getDevice(ccd)

        ccd_connect = self.device_ccd.getSwitch("CONNECTION")

        while not ccd_connect:
            time.sleep(0.5)
            ccd_connect = self.device_ccd.getSwitch("CONNECTION")
        if not self.device_ccd.isConnected():
            ccd_connect[0].s = PyIndi.ISS_ON  # the "CONNECT" switch
            ccd_connect[1].s = PyIndi.ISS_OFF  # the "DISCONNECT" switch
            self.sendNewSwitch(ccd_connect)


    def newDevice(self, d):
        self.device = d

    def newProperty(self, p):
        if p.getName() == "CONNECTION":
            self.connectDevice(self.device.getDeviceName())

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
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

