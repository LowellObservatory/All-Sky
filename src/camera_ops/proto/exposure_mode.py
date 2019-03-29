#!/usr/bin/env python 

from astropy.io import fits
import sys
import numpy as np
from scipy import stats
from glob import glob
from datetime import datetime
from pathlib import Path
from time import sleep

basedir = str(Path.home()) + '/'
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basedir + utdate + '/'
imgfile = sorted(glob(datapath + 'TARGET_*.fit'))[90:-90] 


class Mode:
    def __init__(self):
        self.meanmode = []

    def workfunc(self, imgfile):
        datain = fits.open(imgfile)
        data = datain[0].data
        data = data[0:1000, 200:1215]

        final = data.reshape(1000, 1015)
        lx, ly = final.shape
        X, Y = np.ogrid[0:lx, 0:ly]
        A = 0  # vertical, greater value moves down
        B = 0  # horizontal, greater value moves right
        C = 4.00  # radius, larger value tightens radius
        mask = (A + (X - lx / 2)) ** 2 + (B + (Y - ly / 2)) ** 2 > ((lx * ly) / C)
        final[mask] = 0

        num_bins = 1000
        xmode = np.max(stats.mode(final)[0])
        self.meanmode.append(xmode)
        sleep(0.0625)
        return xmode

if __name__ == "__main__":
    fmode = Mode()
    for ic in range(0, len(imgfile)):
        nextimg = imgfile[ic]
        print('%03d' % ic + ' ' + str(fmode.workfunc(nextimg)))

    avgmode = np.mean(fmode.meanmode)
    print(f'Mean of the modes: {avgmode:4.2f}')
