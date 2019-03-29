#!/usr/bin/env python 

from astropy.io import fits
import sys
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from glob import glob
from datetime import datetime
from pathlib import Path
from time import sleep
plt.style.use('dark_background')

basedir = str(Path.home()) + '/'
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basedir + utdate + '/'
imgfile = sorted(glob(datapath + 'TARGET_*.fit'))[90:-90] 

imgcount = 0


class DoPlot:
    def __init__(self):
        self.fig = plt.figure(figsize=(11.0, 11.0), dpi=100)
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
        mode = np.max(stats.mode(final)[0])

        plt.xlabel('ADU')
        plt.ylabel('Frequency')
        plt.title(str(imgfile[-17:]) + '  ' + str(mode))
        self.meanmode.append(mode)
        print(str(imgfile[-17:]) + '  ' + str(mode))
        plt.xlim([100, 6000])
        # plt.xlim([100, 41000])
        plt.ylim([0, 210000])
        # plt.ylim([0, 100000])
        plt.hist(final.flat, num_bins)
        plt.tight_layout()
        self.fig.canvas.draw()
        self.fig.show()


if __name__ == "__main__":
    dp = DoPlot()
    for ic in range(0, len(imgfile)):
        plt.pause(0.0625)
        dp.fig.clear()
        nextimg = imgfile[ic]
        dp.workfunc(nextimg)

avgmode = np.mean(dp.meanmode)
print(f'Mean of the modes: {avgmode:4.2f}')
plt.show()
