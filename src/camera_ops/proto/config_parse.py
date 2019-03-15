#!/home/lpb/anaconda3/bin/python

import json
from pprint import pprint

with open('camera.json') as f:
    data = json.load(f)

camname = data['camera']['camid'] 
camloc = data['camera']['locname']
campath = data['camera']['path']

# 0 = local, 1 = remote
path_input = 0
pathnum = data['camera']['pathno'][path_input]

lat = data['locgeo']['lat'] 
lon = data['locgeo']['lon']
elev = data['locgeo']['elev']

print(str(camname) + ', ' + str(camloc) + ', ' + str(campath[pathnum]) + ', ' + str(pathnum))
print(str(lat) + ', ' + str(lon) + ', ' + str(elev))
