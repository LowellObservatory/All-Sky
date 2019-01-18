#!/home/sel/anaconda3/bin/python

from indi_interface import IndiClient
import time as tm
from datetime import datetime
import os
from glob import glob
import sys
from astropy.io import fits
from subprocess import Popen, PIPE
# from pathlib import Path


'''
if len(sys.argv) < 2:
    print('Usage: cmd_sx.py <exptime>')
    sys.exit()
'''
'''
disp_flag = input('Do you want to display images? [y/n]: ')

if disp_flag == 'y':
    from pyds9 import *
    d = DS9()
'''

# from pyds9 import *
# d = DS9()
exptime = 0
datapath = '/home/sel/20190118'
filename = '20190118_0001.fits'

# indiclient = IndiClient(exptime, datapath, filename)
# indiclient.setServer("localhost", 7624)

# if (not(indiclient.connectServer())):
#     print("No indiserver running on " + indiclient.getHost() + ":" + str(indiclient.getPort()) + " - Try to run")
#     sys.exit(1)


basepath = os.environ['HOME'] + '/'
expcfg = basepath + 'scripts/exp.cfg'
# expcfg = sys.argv[1]
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basepath + utdate + '/'

if not os.path.exists(datapath):
    try:
        os.makedirs(datapath)
        tm.sleep(1)
    except OSError as e:
        print(e)

ninseries = 524
for i in range(0, ninseries):
    fifofile = '/tmp/indififo'
    #Path(fifofile).touch()
    try:
        os.mkfifo(fifofile)
    except FileExistsError as e:
        print(str(e) + ' fifo file already exists')

    tstamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%s')[0:22]
    print(str(tstamp) + ' : datapath: ' + str(datapath))
    print('Taking exposure ' + str(i + 1) + ' of ' + str(ninseries))
    exptime = expcfg
    f = open(expcfg, 'r')
    exptime = f.read()
    f.close()
    filelist = sorted(glob(datapath + utdate + '_*.fits'))

    print(exptime)

    if len(filelist) == 0:
        filename = utdate + '_0001.fits'
    elif len(filelist) >= 1:
        lastfile = sorted(glob(datapath + utdate + '_*.fits'))[-1]
        print('lastfile: ' + str(lastfile))
        fileseq = int(lastfile[-9:-5])
        print('fileseq: ' + str(fileseq))
        fileseq += 1     
        print('fileseq: ' + str(fileseq))
        filename = utdate + '_' + '%04d' % fileseq + '.fits'
  
    print(filename)
    tm.sleep(0.1)

    # indiclient = IndiClient()

    indiclient = IndiClient(exptime, datapath, filename)
    os.remove(fifofile)
    # indiclient.setServer("localhost", 7624)

    # connect to indi server
    print("Connecting to indiserver")
    if (not(indiclient.connectServer())):
        print("No indiserver running on " + indiclient.getHost() + ":" + str(indiclient.getPort()) + " - Try to run")
        # Popen(['/usr/bin/sh', '-c', './start_indi_server &'], stdout=PIPE)
        sys.exit(1)

    sleep_one = float(exptime) + 1.0
    tm.sleep(sleep_one)
    # os.remove(fifofile)

    # indiclient.disconnectServer()
    # tm.sleep(0.1)
    # data, prihdr = fits.getdata(datapath + filename, header=True)
    # hdul = fits.open(datapath + filename)
    # hdr = hdul[0].header

    # tstamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%s')[0:22]
    # prihdr['OBJECT'] = (tstamp)
    # fits.writeto(datapath + filename, data, prihdr, overwrite=True)
    # hdr['OBJECT'] = tstamp  # Does not work
    # hdr.set('OBJECT', tstamp)
    # fits.setval(datapath + filename, 'OBJECT', value=tstamp)
    # tm.sleep(0.1)
    
    '''
    if disp_flag == 'y':
        d.set("file " + datapath + filename)
    '''
    #d.set("file " + datapath + filename)
    # sleep_two = 63.0 - float(sleep_one) 
    # sleep_two = 1.66 - float(sleep_one) 
    sleep_two = 1.0
    tm.sleep(sleep_two)
    # openfiles = Popen(['/usr/bin/sh', '-c', 'lsof | grep STREAM | wc -l'], stdout=PIPE)
    # openfiles = Popen(['/usr/bin/sh', '-c', 'lsof | grep indi_sx_c | grep FIFO | wc -l'], stdout=PIPE)
    # ofreturn = openfiles.communicate()[0].decode()
    # print(ofreturn)

