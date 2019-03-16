#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi
import sys


class NumberProp():
    def __init__(self):
        pass

    def get_number(self, prop_val):
        getnum = ic.device_ccd.getProperty(prop_val)
        number = getnum.getNumber()

        if not number:
            print('Perhaps not a number property')
            sys.exit()

        for i in number:
            print(i.name, i.value)
              

np = NumberProp()
ic = IndiClient()

prop_val = sys.argv[1]
np.get_number(prop_val)
