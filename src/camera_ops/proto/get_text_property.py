#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi
import sys


class NumberProp():
    def __init__(self):
        pass

    def get_number(self, prop_val):
        getnum = ic.device_ccd.getProperty(prop_val)
        try:
            number = getnum.getText()
        except AttributeError as e:
            print('The driver does not support this feature')
            print(str(e))
            sys.exit()

        if not number:
            print('Perhaps not a number property')
            sys.exit()

        for i in number:
            print(i.name, i.text)   
              

np = NumberProp()
ic = IndiClient()

if len(sys.argv) < 2:
    print('You must enter a property name as an argument')
    sys.exit()

prop_val = sys.argv[1]
np.get_number(prop_val)
