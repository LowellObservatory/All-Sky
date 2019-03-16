#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi
import sys


class SwitchProp():
    def __init__(self):
        pass

    def get_switch(self, prop_val):
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


sp = SwitchProp()
ic = IndiClient()

prop_val = sys.argv[1]
gs.get_switch(prop_val)
