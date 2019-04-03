#!/usr/bin/env python

from subprocess import Popen, PIPE
import os
import glob
from time import *
import time as tm
import numpy as np
import ephem

sleeptime = 60.0
cfgfile = '/home/sel/scripts/exp.cfg'
flagstaff = ephem.Observer()
flagstaff.lat, flagstaff.lon = '35.09708', '-111.5367'
flagstaff.elevation = 2206

while True:
    utdate = strftime('%Y%m%d', gmtime())
    utcdate = strftime('%Y/%m/%d', gmtime())

    moon = ephem.Moon()
    moon.compute(flagstaff.date, epoch=flagstaff.date)
    moon_loc = ephem.Moon()
    moon_loc.compute(flagstaff)
    moon_alt = moon_loc.alt
    moondms = np.degrees(ephem.degrees(moon_alt))
    moonflt = '{0:1.4f}'.format(moondms)

    sun = ephem.Sun()
    sun.compute(flagstaff)
    sun_alt = sun.alt
    sundms = np.degrees(ephem.degrees(sun_alt))
    sunflt = '{0:1.4f}'.format(sundms)
    sunstr = sunflt
    
    # If no data has been written yet return empty seqnum. Wait until the first
    # data is written. 
    try:
        lastfile = sorted(glob.glob('/home/sel/' + utdate + '/' + utdate + '_*.fits'))[-1]
        seqnum = lastfile[28:32]
    except FileNotFoundError:
        seqnum = ""

    lastjpg = '/home/sel/allsky/subframe.jpg'
    os.environ['lastjpgsh'] = lastjpg
    meanval1 = Popen(['/bin/sh', '-c', 'convert $lastjpgsh -format "%[mean]" info:'], stdout=PIPE)
    stdval1 = Popen(['/bin/sh', '-c', 'identify -verbose $lastjpgsh | grep deviation | cut -c27-30'], stdout=PIPE)
    meanval1 = meanval1.communicate()[0]
    stdadu = stdval1.communicate()[0]

    try:
        stdadu = float(stdadu)
    except (TypeError, ValueError):
        stdadu = 0.0

    meanadu = int(float(meanval1))

    expval = 0
    fp = open(cfgfile)
    for i, line in enumerate(fp):
        if i == 0:
            expval = line
            expval = float(expval)
            expval = '{0:1.4f}'.format(expval)
    fp.close()
    dtstamp = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    adudiff = 0

    # Exposure time algorithm is based on the measured ADU of the unprocessed jpeg subframe image
    # This section for ADU above target ADU levels
    newexpval = 0 
    if meanadu > 29000:
        adudiff = meanadu - 29000
        if 500 < adudiff < 1500:
            newexpval = (float(expval) + (float(expval) / 1.05)) / 2.0
            if newexpval < 2.5 and float(sunflt) <= -6:
                newexpval = 2.5
            elif newexpval < 30.0 and float(sunflt) <= -12:
                newexpval = 30.0
            elif newexpval < 60.0 and float(sunflt) <= -18.0:
                newexpval = 60.0
            elif newexpval < 0.08 and float(sunflt) > -1.5:
                newexpval = 0.08

        elif 1500 <= adudiff < 2500:
            newexpval = (float(expval) + (float(expval) / 1.08)) / 2.0
            if newexpval < 2.5 and float(sunflt) <= -6:
                newexpval = 2.5    moon = ephem.Moon()
    moon.compute(flagstaff.date, epoch=flagstaff.date)
    moon_loc = ephem.Moon()
    moon_loc.compute(flagstaff)
    moon_alt = moon_loc.alt
    moondms = np.degrees(ephem.degrees(moon_alt))
    moonflt = '{0:1.4f}'.format(moondms)
    moonstr = str(moonflt)
    mphase = moon.phase
    mphaseflt = '{0:1.1f}'.format(mphase)
            elif newexpval < 30.0 and float(sunflt) <= -12:
                newexpval = 30.0
            elif newexpval < 60.000 and float(sunflt) <= -18.0:
                newexpval = 60.0
            elif newexpval < 0.08 and float(sunflt) > -1.5:
                newexpval = 0.08
 
        elif 2500 <= adudiff < 10000:
            newexpval = (float(expval) + (float(expval) / 1.22)) / 2.0
            if newexpval < 2.5 and float(sunflt) <= -6:
                newexpval = 2.5
            elif newexpval < 30.0 and float(sunflt) <= -12:
                newexpval = 30.0
            elif newexpval < 60.0 and float(sunflt) <= -18.0:
                newexpval = 60.0
            elif newexpval < 0.08 and float(sunflt) > -1.5:
                newexpval = 0.08

        elif 10000 <= adudiff < 21000:
            newexpval = (float(expval) + (float(expval) / 1.53)) / 2.0
            if newexpval < 2.5 and float(sunflt) <= -6:
                newexpval = 2.5
            elif newexpval < 30.0 and float(sunflt) <= -12:
                newexpval = 30.0
            elif newexpval < 60.0 and float(sunflt) <= -18.0:
                newexpval = 60.0
            elif newexpval < 0.08 and float(sunflt) > -1.5:
                newexpval = 0.08

        elif 21000 <= adudiff < 27000:
            newexpval = (float(expval) + (float(expval) / 1.72)) / 2.0
            if newexpval < 2.5 and float(sunflt) <= -6:
                newexpval = 2.5
            elif newexpval < 30.0 and float(sunflt) <= -12:
                newexpval = 30.0
            elif newexpval < 60.0 and float(sunflt) <= -18.0:
                newexpval = 60.0
            elif newexpval < 0.08 and float(sunflt) > -1.5:
                newexpval = 0.08

        elif adudiff >= 27000:
            newexpval = float(expval) / 1.72
            if newexpval < 2.5 and float(sunflt) <= -6:
                newexpval = 2.5
            elif newexpval < 30.0 and float(sunflt) <= -12.0:
                newexpval = 30.0
            elif newexpval < 60.0 and float(sunflt) <= -18.0:
                newexpval = 60.0
            elif newexpval < 0.08 and float(sunflt) > -1.5:
                newexpval = 0.08
        else:
            newexpval = expval
            newexpval = float(newexpval)

        adudiff = str('+' + str(adudiff))
        content = str(newexpval)[0:7]
        lines = [content + '\n']

        # For ADU values under target ADU 
    elif meanadu < 28000:
        adudiff = 28000 - meanadu
        if 500 < adudiff < 1500:
            newexpval = (float(expval) + (float(expval) * 1.05)) / 2.0
            if newexpval > 60.0:
                newexpval = 60.0
            if newexpval < 0.08:
                newexpval = 0.08
        elif 1500 <= adudiff < 2500:
            newexpval = (float(expval) + (float(expval) * 1.08)) / 2.0
            if newexpval > 60:
                newexpval = 60
            if newexpval < 0.08:
                newexpval = 0.08
        elif 2500 <= adudiff < 10000:
            newexpval = (float(expval) + (float(expval) * 1.22)) / 2.0
            if newexpval > 60.0:
                newexpval = 60.0
            if newexpval < 0.08:
                newexpval = 0.08
        elif 10000 <= adudiff < 21000:
            newexpval = (float(expval) + (float(expval) * 1.53)) / 2.0
            if newexpval > 60.0:
                newexpval = 60.0
            if newexpval < 0.08:
                newexpval = 0.08
        elif adudiff >= 21000:
            newexpval = (float(expval) + (float(expval) * 1.72)) / 2.0
            if newexpval > 60.0:
                newexpval = 60.0
            if newexpval < 0.08:
                newexpval = 0.08
        else:
            newexpval = expval

        adudiff = str('-' + str(adudiff))

        content = str(newexpval)[0:7]
        lines = content + '\n'
        # End exposure time algorithm

    if sleeptime < 60.0:
        sleeptime = 60.0

    # When exposure time of 60 seconds is reached start levels.py unless it is
    # already running and only if the moon is below the horizon
    # Don't write a change to exp.cfg if the above conditions exist.

    if float(newexpval) == 60.0 and float(moonflt) <= 0.0 and float(sunflt) < -18.0 and seqnum.isdigit() is True:
        Popen(['/bin/sh', '-c', '/home/sel/bin/auto_levels &'], stdout=PIPE)
        tm.sleep(30.0)

        # exit and keep the exposure set at 60.0 seconds
        exit(0)
    elif float(newexpval) == 60.0 and float(sunflt) <= -18.0 and seqnum.isdigit() is True:
        content = str(newexpval)[0:7]
        lines = content + '\n'
        expfile = open('/home/sel/scripts/exp.cfg', 'w')
        expfile.writelines(lines)
        expfile.close()

        # start the levels.py script once exposure time of 60 seconds is reached.
        # Once levels.py is started exit this program.

        Popen(['/bin/sh', '-c', '/home/sel/bin/auto_levels &'], stdout=PIPE)
        tm.sleep(60.0)

        # exit so that exposure stays set at 60.0 seconds
        exit(0)
    else:
        if float(newexpval) < 0.08:
            newexpval = 0.08
 
        content = str(newexpval)[0:7]
        lines = content + '\n'
        expfile = open('/home/sel/scripts/exp.cfg', 'w')
        expfile.writelines(lines)
        expfile.close()
    
    sleep(sleeptime)
