
from time import sleep
import numpy as np
import xml.etree.ElementTree as et
import stomp
from stomp.listener import ConnectionListener
from pathlib import Path

basedir = str(Path.home()) + '/'

"""
Prototype of the tcs listener
for proto_LOFITS
"""

def parse_xml(body):
    try:
        # For testing, if reading from a file
        # tree = et.parse(basedir + 'log.txt')
        # root = tree.getroot()
        # If reading from message broker use et.fromstring()
        root = et.fromstring(body)
        for child in root:
            decd, decm, decs, decss = int(root[11][3][0][0].text), int(root[11][3][0][1].text), \
                int(root[11][3][0][2].text.split('.')[0]), int(root[11][3][0][2].text.split('.')[1])

            rah, ram, ras, rass = int(root[11][3][4][0].text), int(root[11][3][4][1].text), \
                int(root[11][3][4][2].text.split('.')[0]), int(root[11][3][4][2].text.split('.')[1])

            '''
            lsth = root[9][0][0].text, lstm = root[9][0][1].text, lsts = root[9][0][2].text
            utc = root[9][1].text
            zd = root[10][2][0].text
            am = root[10][3].text
            azdeg, azmin, azsec = root[11][1][0][0].text, root[11][1][0][1].text, root[11][1][0][2].text 
            alth, altm, alts = root[11][1][1][0].text, root[11][1][1][1].text, root[11][1][1][2].text
            hah, ham, has = root[11][2][0].text, root[11][2][1].text, root[11][2][2].text
            '''
    except ElementTree.ParseError as e:
        print(e)
 
    rastr = f"{rah:02d}:{ram:02d}:{ras:02d}.{rass:02d}"
    decstr = f"{decd:02d}:{decm:02d}:{decs:02d}.{decss:02d}"
    return rastr, decstr


class Error(Exception):
    pass


class subscriber(ConnectionListener):
    def on_message(self, headers, body):
        try:
            parse_xml(body)
        except ConnectionError:
            print(headers)

        sleep(60)  # We only need the information once per minute, so wait 60 seconds.


default_host = ''
tcsTelemetry = 'TCS.TCSSharedVariables.TCSHighLevelStatusSV.TCSTcsStatusSV'
conn = stomp.Connection([(default_host, 61613)])
conn.set_listener('tcs-subscriber', subscriber())
conn.start()
conn.connect()
conn.subscribe("/topic/" + tcsTelemetry, 123)
slptm = 60
conn.disconnect()

while True:
    sleep(slptm)
