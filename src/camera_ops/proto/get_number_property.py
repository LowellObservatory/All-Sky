#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi
import sys

class FrameType():
    def __init__(self):
        pass

    def send_new_frame_type(self, prop_val):
        getnum = ic.device_ccd.getProperty(prop_val)
        number = getnum.getNumber()

        if not number:
            print('Perhaps not a number property')
            sys.exit()

        for i in number:
            print(i.name, i.value)
              

ft = FrameType() 
ic = IndiClient()

prop_val = sys.argv[1]
ft.send_new_frame_type(prop_val)
