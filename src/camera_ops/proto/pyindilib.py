import PyIndi
import time
import sys

class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.setServer("localhost", 7624)

        if (not(self.connectServer())):
            print("No indiserver running on " + self.getHost() + ":" + str(self.getPort()) + " - Try to run")
            sys.exit(1)

        ccd = "SX CCD SuperStar"
        self.device_ccd = self.getDevice(ccd)

        while not(self.device_ccd):
            time.sleep(0.5)
            self.device_ccd = self.getDevice(ccd)

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

