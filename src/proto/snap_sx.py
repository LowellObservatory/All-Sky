#!/usr/bin/env python

from indi_interface import IndiClient
import time as tm
from datetime import datetime
import os
from glob import glob
import sys
from astropy.io import fits

if len(sys.argv) < 2:
    print('Usage: find_and_focus_sx.py <exptime>')
    sys.exit()

disp_flag = input('Do you want to display images? [y/n]: ')

if disp_flag == 'y':
    from pyds9 import *
    d = DS9()

basepath = os.environ['HOME'] + '/'
expcfg = sys.argv[1]
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basepath + utdate + '/'

if not os.path.exists(datapath):
    try:
        os.makedirs(datapath)
    except OSError as e:
        print(e)

tstamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(str(tstamp) + ' : datapath: ' + str(datapath))
exptime = expcfg
filelist = sorted(glob(datapath + 'TARGET__*.fit'))

print(exptime)

if len(filelist) == 0:
    filename = 'TARGET__00001.fit'
elif len(filelist) >= 1:
    lastfile = sorted(glob(datapath + 'TARGET__*.fit'))[-1]
    print('lastfile: ' + str(lastfile))
    fileseq = int(lastfile[-8:-4])
    print('fileseq: ' + str(fileseq))
    fileseq += 1     
    print('fileseq: ' + str(fileseq))
    filename = 'TARGET__' + '%05d' % fileseq + '.fit'
  
print(filename)
tm.sleep(0.1)
indiclient = IndiClient(exptime, datapath, filename)

indiclient.setServer("localhost", 7624)

# connect to indi server
print("Connecting to indiserver")
if (not(indiclient.connectServer())):
    print("No indiserver running on " + indiclient.getHost() + ":" + str(indiclient.getPort()) + " - Try to run")
    sys.exit(1)

sleep_one = float(exptime) + 1.0
tm.sleep(sleep_one)
indiclient.disconnectServer()
tm.sleep(0.05)
data, prihdr = fits.getdata(datapath + filename, header=True)

tstamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
prihdr['OBJECT'] = (tstamp)
fits.writeto(datapath + filename, data, prihdr, overwrite=True)
tm.sleep(0.05)
if disp_flag == 'y':
    d.set("file " + datapath + filename)

