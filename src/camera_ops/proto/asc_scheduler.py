
from astropy.coordinates import EarthLocation, get_sun, AltAz
from astropy.time import Time
import json
config_file = '/home/sel/indidev/config.json'

class ObsScheduler:
    def __init__(self):
        self.sun_angle = 0
        self.sun_deg = 0
        with open(config_file) as f:
            data = json.load(f)

        self.location = EarthLocation.from_geodetic(data['locgeo']['lon'], data['locgeo']['lat'], data['locgeo']['elev'])
        
    def sunang(self):
        altaz = AltAz(location=self.location, obstime=Time.now())
        sun = get_sun(Time.now())
        # file2read = '/home/sel/indidev/srss'
        # f = open(file2read, 'r')
        # self.sun_deg = f.read()
        self.sun_deg = float(f'{sun.transform_to(altaz).alt.deg:2.2f}')
        # f.close()
        return self.sun_deg

