#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi

class FrameType():
    def __init__(self):
        pass

    def send_new_frame_type(self, newswitch):
        ccd_connect = ic.device_ccd.getProperty("CCD_FRAME_TYPE")
        switch = ccd_connect.getSwitch()

        if newswitch == 'Light':
            switch[0].s = PyIndi.ISS_ON
            switch[1].s = PyIndi.ISS_OFF
            switch[2].s = PyIndi.ISS_OFF
            switch[3].s = PyIndi.ISS_OFF
        elif newswitch == 'Bias':
            switch[0].s = PyIndi.ISS_OFF
            switch[1].s = PyIndi.ISS_ON
            switch[2].s = PyIndi.ISS_OFF
            switch[3].s = PyIndi.ISS_OFF
        elif newswitch == 'Dark':
            switch[0].s = PyIndi.ISS_OFF
            switch[1].s = PyIndi.ISS_OFF
            switch[2].s = PyIndi.ISS_ON
            switch[3].s = PyIndi.ISS_OFF
        elif newswitch == 'Flat':
            switch[0].s = PyIndi.ISS_OFF
            switch[1].s = PyIndi.ISS_OFF
            switch[2].s = PyIndi.ISS_OFF
            switch[3].s = PyIndi.ISS_ON

        ic.sendNewSwitch(switch)


ft = FrameType() 
ic = IndiClient()

