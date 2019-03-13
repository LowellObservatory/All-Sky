#!/usr/bin/env python

from subprocess import Popen, PIPE
from datetime import datetime

utdate = datetime.utcnow().strftime('%Y%m%d')
logfile = '/home/sel/' + utdate + '_indi.log'

ispid = Popen(['/bin/sh', '-c', 'pgrep indiserver'], stdout=PIPE)
pidis = ispid.communicate()[0].decode()

if not pidis:
    print('The indiserver is not running. Will attempt to start now...')
    Popen(['/bin/sh', '-c', 'mkfifo /tmp/indififo'], stdout=PIPE)
    Popen(['/bin/sh', '-c', '/usr/bin/indiserver -vvv -f /tmp/indififo indi_sx_ccd 2> ' + logfile], stdout=PIPE)

else:
    print('The indiserver is already running.')

