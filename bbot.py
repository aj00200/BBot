#! /usr/bin/python
'''BBot is a free IRC bot which was designed to be modular and fast.
It is licensed under the GNU GPL v3 license as well as the MIT license.
See the LICENSE file for more details'''

VERSION = '7.0.3'
import sys
import asyncore

import config
import api

if __name__ == '__main__':
    if '--help' in sys.argv:
        print('Current command line options are:')
        print('  --local-config - Reads config.cfg from current directory')
        print('  --user-config  - Reads config.cfg from the home directory')
    else:
        print(' * Connecting to %s on port %s' % (config.network, config.port))
        api.backend.connect(config.network, config.port, config.ssl)
        asyncore.loop()
