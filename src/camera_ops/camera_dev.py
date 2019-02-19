import time
from device_dev import Device
import PyIndi
from datetime import datetime
from pathlib import Path
from glob import glob

basedir = str(Path.home()) + '/'
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basedir + utdate + '/'


class CameraChangeSettingsStep:
    def __init__(self, camera, frame_type = None, controls = None, numbers = None, switches = None):
        self.camera = camera
        self.frame_type = frame_type
        self.controls = controls
        self.numbers = numbers
        self.switches = switches

    def run(self):
        if self.frame_type:
            self.camera.set_frame_type(self.frame_type)
        if self.controls:
            self.camera.set_controls(self.controls)
        if self.numbers:
            for control_name, control_values in self.numbers.items():
                self.camera.set_number(control_name, control_values)
        if self.switches:
            for control_name, control_values in self.switches.items():
                self.camera.set_switch(control_name, control_values['on'] if 'on' in control_values else [], control_values['off'] if 'off' in control_values else [])

    def __str__(self):
        values = [['frame_type', self.frame_type], ['controls', self.controls], ['numbers', self.numbers], ['switches', self.switches]]
        values = [': '.join([x[0], str(x[1])]) for x in values if x[1]]
        return 'Change camera settings: {0}'.format(', '.join(values))

    def __repr__(self):
        return self.__str__()


class Camera(Device):
    def __init__(self, name, indi_client, connect_on_create = True):
        Device.__init__(self, name, indi_client)
        if connect_on_create:
            self.connect()
    
    def img_acquire(self, exposure, sync=True, timeout=None):
        if not timeout:
            timeout = exposure * 1.5 + 60
        
        try:
            path = datapath
            lastimg = sorted(glob(datapath + utdate + '_*.fits'))[-1][-9:-5]
            seq = int(lastimg) + 1
            seqno = '%04d' % seq
            prefix = datetime.utcnow().strftime('%Y%m%d') + '_' + str(seqno)
        except IndexError:
            path = datapath
            prefix = datetime.utcnow().strftime('%Y%m%d') + '_0001'
    
        self.set_text('UPLOAD_SETTINGS', {'UPLOAD_DIR': path, 'UPLOAD_PREFIX': prefix})
        self.set_number('CCD_EXPOSURE', {'CCD_EXPOSURE_VALUE': exposure}, sync=sync, timeout=timeout)

    prefix = datetime.utcnow().strftime('%Y%m%d') + '_0001'
    def set_upload_path(self, path, prefix=prefix):
        self.set_text('UPLOAD_SETTINGS', {'UPLOAD_DIR': path, 'UPLOAD_PREFIX': prefix})

    def set_header(self, keyword, value, keyword2, value2):
        self.set_text('FITS_HEADER', {keyword: value, keyword2: value2})

    def ccd_info(self):
        return self.values('CCD_INFO', 'number')

    def frame_type(self):
        return self.switch_values('CCD_FRAME_TYPE')

    def set_frame_type(self, frame_type):
        self.set_switch('CCD_FRAME_TYPE', [frame_type])

    def controls(self):
        return self.values('CCD_CONTROLS', 'number')

    def set_controls(self, exposure):
        self.set_number('CCD_CONTROLS', controls)

    # Experimental lpb, 2019.02.08
    # def set_exposure(self, exposure):
    #    return self.set_text('CCD_EXPOSURE', {'CCD_EXPOSURE_VALUE': exposure})

    def set_upload_to(self, upload_to = 'local'):
        upload_to = {'local': 'UPLOAD_LOCAL', 'client': 'UPLOAD_CLIENT', 'both': 'UPLOAD_BOTH'}[upload_to]
        self.set_switch('UPLOAD_MODE', [upload_to] )

    def exposure_range(self):
        ctl = self.get_control('CCD_EXPOSURE', 'number')[0]
        return {
            'minimum': ctl.min,
            'maximum': ctl.max,
            'step': ctl.step
        }

    def __str__(self):
        return 'INDI Camera "{0}"'.format(self.name)

    def __repr__(self):
        return self.__str__()
