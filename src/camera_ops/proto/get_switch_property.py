#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi
import sys

class FrameType():
    def __init__(self):
        pass

    def send_new_frame_type(self, prop_val):
        prop_val = ic.device_ccd.getProperty(prop_val)

        switch = prop_val.getSwitch()
        if not switch:
            print('Perhaps not a switch value')
            sys.exit()
       
        try:
            if switch[0].s == 1:
                print(switch[0].name)
            elif switch[1].s == 1:
                print(switch[1].name)
            elif switch[2].s == 1:
                print(switch[2].name)
            elif switch[3].s == 1:
                print(switch[3].name)
        except (IndexError):
            print('Maybe not a switch variable?')

              

ft = FrameType() 
ic = IndiClient()

prop_val = sys.argv[1]
ft.send_new_frame_type(prop_val)
