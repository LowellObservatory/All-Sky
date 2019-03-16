#!/usr/bin/env python

from subprocess import Popen, PIPE
from datetime import datetime
import os

utdate = datetime.utcnow().strftime('%Y%m%d')
logfile = '/home/sel/' + utdate + '_indi.log'

ispid = Popen(['/bin/sh', '-c', 'pgrep indiserver'], stdout=PIPE)
pidis = ispid.communicate()[0].decode()

if not pidis:
    print('The indiserver is not running. Will attempt to start now...')
    try:
        os.mkfifo('/tmp/indififo')
        Popen(['/bin/sh', '-c', '/usr/bin/indiserver -f /tmp/indififo indi_sx_ccd'], stdout=PIPE)
    except FileExistsError:
        # Popen(['/bin/sh', '-c', '/usr/bin/indiserver -vvv -f /tmp/indififo indi_sx_ccd 2> ' + logfile], stdout=PIPE)
        Popen(['/bin/sh', '-c', '/usr/bin/indiserver -f /tmp/indififo indi_sx_ccd'], stdout=PIPE)
    except OSError:
        Popen(['/bin/sh', '-c', '/usr/bin/indiserver indi_sx_ccd'], stdout=PIPE)
else:
    exit('The indiserver is already running.')
