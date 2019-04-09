
from datetime import datetime
from glob import glob
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon
from astropy.time import Time
from astropy.io import fits
from astropy.io.fits import ImageHDU
import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)
warnings.filterwarnings('ignore', category=Warning, append=True)
from astroplan import Observer
import xml.etree.ElementTree as ET
import urllib.request
from xml.dom import minidom
from pathlib import Path
import base64
from pyds9 import DS9

"""
protoLOFITS
The fits header builder for Lowell Allsky camera(s)
2019/04/08
"""

basedir = str(Path.home()) + '/'
utdate = datetime.utcnow().strftime('%Y%m%d')
datapath = basedir + utdate


class FitsOps:
    def __init__(self):
        self.seqno = '0001'
        self.tempC, self.rh = 0.0, 0
        self.lststr, self.moonface, self.moonalt, self.sunalt, self.seqnum, self.moonillum, = '', 0, 0, 0, 0, 0
        self.testif = 0

    def environmental(self):
        try:
            url = 'http:///latestsampledata.xml'
            usock = urllib.request.urlopen(url)
            xmldoc = minidom.parse(usock)
            usock.close()
            data = xmldoc.toxml()
            root = ET.fromstring(data)
            tempf = root[2].text
            self.rh = root[19].text
            self.tempC = (5.0 / 9.0) * (float(tempf) - 32)
        except Exception as e:
            print(e)
            self.tempC, self.rh = 0.0, 0

        self.tempC = '%02.1f' % float(self.tempC)
        return self.tempC, self.rh

    def sun_moon(self):
        lat, longit, elev = '34.7443', '-111.4223', 2361  
        loc = EarthLocation.from_geodetic(longit, lat, elev)
        dct = Observer(loc, timezone='US/Mountain')
        now = Time.now()
        altaz = AltAz(location=loc, obstime=now)
        sun = get_sun(now)
        moon = get_moon(now, loc)
        lst = dct.local_sidereal_time(now)
        lst = lst.hms
        lsth, lstm, lsts = str(lst[0]).split('.')[0], str(lst[1]).split('.')[0], str(lst[2]).split('.')[0]
        lstss = str(lst[2]).split('.')[1]
        self.lststr = '%02d' % int(lsth) + ':' + '%02d' % int(lstm) + ':' + '%02d' % int(lsts) + '.' + lstss[0:2]

        moonfz = dct.moon_illumination(now)
        self.moonillum = f'{moonfz * 100:04.1f}' 
        moonget = moon.transform_to(altaz).alt.deg
        self.moonalt = '{:2.4f}'.format(moonget)
        sunget = sun.transform_to(altaz).alt.deg
        self.sunalt = '{:2.4f}'.format(sunget)
        return self.lststr, self.sunalt, self.moonalt, self.moonillum
    
    def fits_header(self, message):
        try:
            lastimg = sorted(glob(datapath + '/' + utdate + '_*.fits'))[-1][-9:-5]
            seq = int(lastimg) + 1
            self.seqno = '%04d' % seq
            seqnum = self.seqno
            datafile = datapath + '/' + datetime.utcnow().strftime('%Y%m%d') + '_' + str(self.seqno) + '.fits'
        except IndexError:
            lastimg = datetime.utcnow().strftime('%Y%m%d') + '_0001.fits'
            datafile = datapath + '/' + lastimg
            seqnum = '0001'

        imgdata = ImageHDU.fromstring(base64.b64decode(message))
        prihdr = imgdata.header

        d = DS9()

        try:
            prihdr['DATE-OBS']
        except KeyError:
            pass

        try:
            self.testif = prihdr['PIXSIZE1']

            # Delete unwanted INDI keywords from header
            del prihdr['TELESCOP']
            del prihdr['OBSERVER']
            del prihdr['OBJECT']
            del prihdr['FRAME']
            del prihdr['SCALE']
            del prihdr['PIXSIZE1']
            del prihdr['PIXSIZE2']
            del prihdr['XBINNING']
            del prihdr['YBINNING']
            del prihdr['INSTRUME']
            del prihdr['COMMENT']

            # Append desired keywords to file header
            prihdr.append(('LST-OBS ', self.sun_moon()[0], 'Local Sidereal Time of exposure start'), end=True)
            prihdr.append(('CREATOR ', 'LOASC_INDI', 'File creator'), end=True)
            prihdr.append(('CAMERA  ', 'SX Superstar 1.10', 'Manufacturer  driver version'), end=True)
            prihdr.append(('MODEL   ', 25, 'Camera model number'), end=True)
            prihdr.append(('PIXSIZE ', 4.65, 'Pixel Size in Microns'), end=True)
            prihdr.append(('CCDSUM  ', '1 1', 'On Chip binned summation'), end=True)
            prihdr.append(('IMGTYPE ', 'OBJECT', 'Image Type'), end=True)
            prihdr.append(('OBJECT  ', 'Sky Above DCT', 'Object Name'), end=True)
            prihdr.append(('OBSERVAT', 'DCT Telescope', 'Observatory'), end=True)
            prihdr.append(('OBSLOCAT', 'Happy Jack, AZ', 'Observatory Location'), end=True)
            prihdr.append(('OBSLAT  ', 34.89708, 'Observatory Latitude (degrees)'), end=True)
            prihdr.append(('OBSLONG ', -111.5367, 'Observatory Longitude (degrees)'), end=True)
            prihdr.append(('OBSALT  ', 2202., 'Observatory Altitude (meters)'), end=True)
            prihdr.append(('INSTRUME', 'DCT_ALLSKY', 'Instrument'), end=True)
            prihdr.append(('SEQNUM  ', int(seqnum), 'File Sequence Number'), end=True)
            prihdr.append(('TEMPAMB ', float(self.environmental()[0]), 'Mean Ambient Temperature in deg C'), end=True)
            prihdr.append(('HUMIDITY', int(self.environmental()[1]), 'Relative Humidity (percent)'), end=True)
            prihdr.append(('SUN_ALT ', float(self.sun_moon()[1]), 'Altitude of Sun (degrees)'), end=True)
            prihdr.append(('MOON_ALT', float(self.sun_moon()[2]), 'Altitude of Moon (degrees)'), end=True)
            prihdr.append(('MOONILLU', float(self.sun_moon()[3]), 'Moon illumination (percent)'), end=True)

            fits.writeto(datafile, imgdata.data, imgdata.header, overwrite=True)

            d.set("file " + datafile)

        except KeyError as e:
            print('error: ' + str(e))
            print('This header has already been processed')
