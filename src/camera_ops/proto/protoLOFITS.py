
from datetime import datetime
import glob
import sys
from pathlib import Path
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon
from astropy.time import Time
from astropy.io import fits
import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)
warnings.filterwarnings('ignore', category=Warning, append=True)
from astroplan import Observer

# import xml.etree.ElementTree as et
# import urllib.request
# from xml.dom import minidom
# import stomp
# from stomp.listener import ConnectionListener

"""
protoLOFITS
The fits header builder for Lowell Allsky camera(s)
2019/04/03
"""

basedir = str(Path.home()) + '/'
utdir = datetime.utcnow().strftime('%Y%m%d')
dpath = basedir + utdir

"""
def environmental():
    try:
        url = 'http:///latestsampledata.xml'
        usock = urllib.request.urlopen(url)
        xmldoc = minidom.parse(usock)
        usock.close()
        data = xmldoc.toxml()
        root = et.fromstring(data)
        tempF = root[2].text
        rh = root[20].text
        tempC = (5.0 / 9.0) * (float(tempF) - 32)
    except Exception as e:
        print(e)
        tempC = 0.0
        rh = 0

    tempC = '%02.1f' % float(tempC)
"""


class FitsOps:
    def __init__(self):
        self.tempF = 52.9
        self.rh = 38
        self.lststr, self.moonface, self.moonalt, self.sunalt, self.seqnum = '', 0, 0, 0, 0

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
        self.moonface = f'{moonfz * 100:04.1f}' 
        moonget = moon.transform_to(altaz).alt.deg
        self.moonalt = '{:2.4f}'.format(moonget)
        sunget = sun.transform_to(altaz).alt.deg
        self.sunalt = '{:2.4f}'.format(sunget)

    def fits_header(self):
        datafile = sorted(glob.glob(dpath + '/' + utdir + '_*.fits'))[-1]
        self.seqnum = datafile[28:32]
        hdulist = fits.open(datafile, mode='update')
        prihdr = hdulist[0].header

        try:
            prihdr['DATE-OBS']
        except KeyError:
            pass

        try:
            prihdr['PIXSIZE1']
        except KeyError:
            print('This header has already been processed')
            sys.exit()

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
        prihdr.append(('LST-OBS ', self.lststr, 'Local Sidereal Time of exposure start'), end=True)
        prihdr.append(('CREATOR ', 'LOASC_INDI', 'File creator'), end=True)
        prihdr.append(('CAMERA  ', 'SX Superstar 1.10', 'Manufacturer  driver version'), end=True)
        prihdr.append(('MODEL   ', 25, 'Camera model number'), end=True)
        prihdr.append(('PIXSIZE ', 4.65, 'Pixel Size in Microns'), end=True)
        prihdr.append(('CCDSUM  ', '1 1', 'On Chip binned summation'), end=True)
        prihdr.append(('IMGTYPE ', 'OBJECT', 'Image Type'), end=True)
        prihdr.append(('OBSERVAT', 'DCT Telescope', 'Observatory'), end=True)
        prihdr.append(('OBSLOCAT', 'Happy Jack, AZ', 'Observatory Location'), end=True)
        prihdr.append(('OBSLAT  ', 34.89708, 'Observatory Latitude (degrees)'), end=True)
        prihdr.append(('OBSLONG ', -111.5367, 'Observatory Longitude (degrees)'), end=True)
        prihdr.append(('OBSALT  ', 2202., 'Observatory Altitude (meters)'), end=True)
        prihdr.append(('INSTRUME', 'DCT_ALLSKY', 'Instrument'), end=True)
        prihdr.append(('SEQNUM  ', int(self.seqnum), 'File Sequence Number'), end=True)
        prihdr.append(('TEMPAMB ', self.tempF, 'Mean Ambient Temperature in deg F'), end=True)
        prihdr.append(('HUMIDITY', int(self.rh), 'Relative Humidity (percent)'), end=True)
        prihdr.append(('SUN_ALT ', float(self.sunalt), 'Altitude of Sun (degrees)'), end=True)
        prihdr.append(('MOON_ALT', float(self.moonalt), 'Altitude of Moon (degrees)'), end=True)
        prihdr.append(('MOONILLU', float(self.moonface), 'Moon illumination (percent)'), end=True)

        hdulist.flush()
        hdulist.close()


fo = FitsOps()
fo.sun_moon()
fo.fits_header()
