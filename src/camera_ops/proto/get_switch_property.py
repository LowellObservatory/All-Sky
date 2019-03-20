#!/home/sel/anaconda3/bin/python

from pyindilib import IndiClient
import PyIndi
import sys


class SwitchProp():
    def __init__(self):
        pass

    def get_switch(self, prop_val):
        prop_val = ic.device_ccd.getProperty(prop_val)
  
        try:
            switch = prop_val.getSwitch()
        except AttributeError as e:
            print('Probably not a switch property', e)
            sys.exit()
     
        """
        try:
            if switch[0].s == 1:
                print(switch[0].name)
            elif switch[1].s == 1:
                print(switch[1].name)
            elif switch[2].s == 1:
                print(switch[2].name)
            #elif switch[3].s == 1:
            #    print('4')
            #    print(switch[3].name)
        except (IndexError, TypeError) as e:
            print('Maybe not a switch property', e)
        
        # print(dir(switch))
        """ 
       
        try:
            for i in range(0, switch.nsp):
                if switch[i].s == 0:
                    print(switch[i].name, ' = Off')
                elif switch[i].s == 1:
                    print(switch[i].name, ' = On')
                else:
                    print(switch[i].name, switch[i].s)
        except AttributeError:
            print('Not a valid switch value')

        

sp = SwitchProp()
ic = IndiClient()

if len(sys.argv) < 2:
    print('You must enter a property name as an argument')
    sys.exit()

prop_val = sys.argv[1]
sp.get_switch(prop_val)
