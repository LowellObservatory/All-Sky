
from indi_interface import IndiClient
import time as tm
from datetime import datetime
import os
from glob import glob
import sys
from astropy.io import fits
from pyds9 import *

if len(sys.argv) < 2:
    print('Usage: find_and_focus_sx.py <exptime>')
    sys.exit()

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

ninseries = 1000
for i in range(0, ninseries):
    tstamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(tstamp) + ' : datapath: ' + str(datapath))
    print('Taking exposure ' + str(i + 1) + ' of ' + str(ninseries))
    exptime = expcfg
    filelist = sorted(glob(datapath + 'TARGET__*.fit'))

    print(exptime)

    filename = 'test.fits' 
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
    tm.sleep(0.1)
    data, prihdr = fits.getdata(datapath + filename, header=True)

    tstamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prihdr['OBJECT'] = (tstamp)
    fits.writeto(datapath + filename, data, prihdr, overwrite=True)
    tm.sleep(0.1)
    d.set("file " + datapath + filename)
    slptime = float(exptime) + 1.0
    tm.sleep(slptime)

