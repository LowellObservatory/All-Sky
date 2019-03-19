
from astropy.coordinates import EarthLocation, get_sun, AltAz
from astropy.time import Time
import json

class ObsScheduler:
    def __init__(self):
        self.sun_angle = 0
        with open('config.json') as f:
            data = json.load(f)

        self.location = EarthLocation.from_geodetic(data['locgeo']['lon'], data['locgeo']['lat'], data['locgeo']['elev'])
        
    def sunang(self):
        altaz = AltAz(location=self.location, obstime=Time.now())
        sun = get_sun(Time.now())
        self.sun_deg = sun.transform_to(altaz).alt.deg

        return self.sun_deg


