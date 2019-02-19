#!/home/sel/anaconda3/bin/python

from camera_dev import Camera, CameraChangeSettingsStep
from indiclient_dev import INDIClient 
import os
from time import sleep
from datetime import datetime
from pathlib import Path
from glob import glob
# from pyds9 import *
# d = DS9()

basedir = str(Path.home()) + '/'
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basedir + utdate + '/'
# curdir = os.getcwd() + '/'

class CameraSetup: 
    def __init__(self, name, camera_name=None, upload_path=None, indi_host=INDIClient.DEFAULT_HOST,
                 indi_port=INDIClient.DEFAULT_PORT):
        self.name = 'inditest'
        self.indi_client = INDIClient(indi_host, indi_port)
        self.camera = 'SX CCD SuperStar'
        self.set_camera(camera_name)

        if not upload_path:
            upload_path = os.path.join(os.environ['HOME'], 'Shots', name)
        print('Will save fits file into {0}'.format(upload_path))
        self.upload_path = upload_path
        print('26: self.upload_path: ' + str(self.upload_path))

    @property
    def devices(self):
        return self.indi_client.device_names

    def set_camera(self, camera_name, timeout=60):
        if not camera_name:
            time.sleep(1)
            print('Camera name cannot be empty. Available devices: {0}'.format(', '.join(self.devices)))
            self.camera = None
            return
        self.camera = Camera(camera_name, self.indi_client)

    def acquire(self, rangeof):
        for i in range(1, int(rangeof) + 1):
            expfile = '/home/sel/indidev/' + 'exp.cfg'
            of = open(expfile, 'r')
            exposure = of.read()
            of.close()

            self.camera.img_acquire(float(exposure), sync=True, timeout=None)

            if float(exposure) > 0.01 and float(exposure) < 60.0:
                pause = 61.0 - float(exposure)
            elif float(exposure) == 60.0:
                pause = 1 
            elif float(exposure) < 0.01:
                pause = 1

            if i == rangeof:
                pause = 0

            print(datetime.utcnow().strftime('%H:%M:%S') + ': ' + str(pause))
            lastimg = sorted(glob(datapath + utdate + '_*.fits'))[-1]
            # d.set("file " + lastimg)
            sleep(pause)

    def change_settings(self, frame_type = None , controls = None, numbers = None, switches = None):
        return (self.camera.set_frame_type('FRAME_LIGHT'), 
                self.camera.set_upload_to('local'), 
                self.camera.set_header('FITS_OBSERVER', 'Bright', 'FITS_OBJECT', 'Camera tests'), 
                self.camera.set_upload_path(self.upload_path)) 

    def test(self, exposure):
        self.camera.set_exposure(exposure)

    def __str__(self):
        to_s = [
            'CameraSetup object "{0}"'.format(self.name),
            'upload path: {0}'.format(self.upload_path),
            self.camera if self.camera else 'Camera not set',
            self.indi_client
        ]
        to_s.extend(self.sequences)
        return '\n'.join([str(s) for s in to_s])

    def __repr__(self):
        return self.__str__()


cs = CameraSetup('dct_allsky', camera_name='SX CCD SuperStar', upload_path=datapath, indi_host='localhost', indi_port=7624)
sleep(1)
cs.set_camera('SX CCD SuperStar')
sleep(1)
cs.change_settings(frame_type = 'FRAME_LIGHT', switches = 'local')
sleep(1)
cs.acquire(rangeof=2)
