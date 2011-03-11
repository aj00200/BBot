#! /usr/bin/python
#This Code is licensed under the GNU GPL v3

VERSION = '7.0.0b5pre'
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
