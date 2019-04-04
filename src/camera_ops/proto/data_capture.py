import PyIndi
import time
import sys
import threading
import time
from datetime import datetime
from glob import glob
from subprocess import Popen, PIPE
from pathlib import Path
import os
from set_frame_type import FrameType
import sys
from asc_scheduler import ObsScheduler

obss = ObsScheduler()
sun_ang = -1.2


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

    def capture(self, nexp, delay):
        sunang = obss.sunang()
        while True:
            if float(sunang) <= sun_ang:
                print('nexp: ' + str(nexp))
                expfile = basdir + "scripts/exp.cfg"
                f = open(expfile, 'r')
                exptime = f.read()
                f.close()
                print('sunang, sun_ang: ' + str(sunang), str(sun_ang))
                print('exposure time: ' + str(exptime))

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
                exposures = [exptime] * int(nexp)

                i = 0
                while i <= len(exposures) and float(sunang) < sun_ang:
                    basedir = str(Path.home()) + '/'
                    utdate = datetime.utcnow().strftime('%Y%m%d')
                    path = basedir + utdate

                    if not os.path.exists(path):
                        try:
                            os.makedirs(path)
                        except OSError as e:
                            print('Error: ' + str(e))

                    self.blobEvent = threading.Event()
                    self.blobEvent.clear()

                    expfile = '{0}scripts/exp.cfg'.format(basedir)
                    f = open(expfile, 'r')
                    exptime = f.read()
                    f.close()

                    self.ccd_exposure[0].value = float(exptime)
                    self.sendNewNumber(self.ccd_exposure)
                    self.blobEvent.wait()

                    ndelay = float(delay) - float(exptime)

                    for blob in ccd_ccd1:
                        # print("name: ", blob.name, " size: ", blob.size, " format: ", blob.format)
                        fitsdata = blob.getblobdata()

                        try:
                            lastimg = sorted(glob(path + '/' + utdate + '_*.fits'))[-1][-9:-5]
                            seq = int(lastimg) + 1
                            self.seqno = '%04d' % seq
                            filename = path + '/' + datetime.utcnow().strftime('%Y%m%d') + '_' \
                                + str(self.seqno) + '.fits'
                        except IndexError:
                            lastimg = datetime.utcnow().strftime('%Y%m%d') + '_0001.fits'
                            filename = path + '/' + lastimg

                        if 0 < i <= len(exposures):
                            ndelay = float(delay) - float(exptime)

                        tstamp = datetime.utcnow().strftime('%H:%M:%S')
                        print(tstamp, filename)

                        f = open(filename, 'wb')
                        f.write(fitsdata)
                        f.close()

                    if i + 1 == len(exposures):
                        time.sleep(float(exptime) + 1)
                    else:
                        time.sleep(ndelay)

                    i += 1
                    sunang = obss.sunang()
            else:
                tstamp = datetime.utcnow().strftime('%H:%M:%S')
                print(tstamp + ' Waiting for sun to reach ' + str(sun_ang))
                time.sleep(60)
                sunang = obss.sunang()


indiclient = IndiClient()
indiclient.setServer("localhost", 7624)


def input_params():
    ft = FrameType()

    # frame_type, nexp, delay = sys.argv[1], sys.argv[2], sys.argv[3]

    frame_type = 'Light'
    nexp = 820
    delay = 61
    ft.send_new_frame_type(frame_type)
    indiclient.capture(nexp, delay)


def chk_redundant():
    processid = Popen(['/bin/sh', '-c', 'pgrep -c data_capture.py'], stdout=PIPE)
    pid = processid.communicate()[0]

    if int(pid) >= 2:
        print('data_capture is already running.')
        print('exit now.\n')
        sys.exit()
    else:
        print('Proceed to main script.')
        input_params()


chk_redundant()
