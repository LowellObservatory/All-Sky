
from pyindilib import IndiClient
import PyIndi
import sys


class TextProp():
    def __init__(self):
        pass

    def get_text(self, prop_val):
        gettext = ic.device_ccd.getProperty(prop_val)
        try:
            text = gettext.getText()
        except AttributeError as e:
            print('The driver does not support this feature')
            print(str(e))
            sys.exit()

        if not text:
            print('Perhaps not a number property')
            sys.exit()

        for i in text:
            print(i.name, i.text)   
              

np = TextProp()
ic = IndiClient()

if len(sys.argv) < 2:
    print('You must enter a property name as an argument')
    sys.exit()

prop_val = sys.argv[1]
np.get_text(prop_val)
