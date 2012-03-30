#! /usr/bin/env python
'''BBot is a free IRC bot which was designed to be modular and fast.
It is licensed under the GNU GPL v3 license as well as the MIT license.
See the README.md file for more details'''

VERSION = '7.5.8'
import sys
import asyncore

import config
import api

if __name__ == '__main__':
    if '--help' in sys.argv or '-v' in sys.argv or '--version' in sys.argv:
        print('BBot the IRC Bot %s' % VERSION)
        print('USAGE: bbot [--config /path/to/config.cfg]')
        sys.exit()
    else:
        api.backend.connect(config.network, config.port, config.ssl)
        api.backend.loop()
