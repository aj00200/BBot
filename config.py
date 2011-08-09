'''Reads config.conf and parses common values for access by other modules'''
import ConfigParser
import sys
import re
import os

try:
    config_file = open(os.getenv('HOME') + '/.BBot/config.cfg', 'r')
    sys.path.insert(1, os.getenv('HOME') + '/.BBot')
    PATH = os.getenv('HOME') + '/.BBot/'
    print('[*] Loaded config.cfg from your home directory')
except IOError:
    print('[*] Error loading config.cfg from your home directory')
    print('    Try running bbot-makeconf if you are on Linux')
    try:
        config_file = open('config.cfg', 'r')
        PATH = ''
        print('[*] Loaded config.cfg from your local directory')
    except IOError:
        print('[*] Error loading config.cfg from your local directory')
        print('    Either create it or run bbot-makeconf if you are on Linux')

c = ConfigParser.ConfigParser()
c.readfp(config_file)

nick = c.get('main', 'nick')
ident = c.get('main', 'ident')
ircname = c.get('main', 'ircname')
username = c.get('main', 'username')
password = c.get('main', 'password')
network = c.get('main', 'network')
port = c.getint('main', 'port')
ssl = c.getboolean('main', 'ssl')
autojoin = c.get('main', 'channels').replace(', ', ',').split(',')
modules = c.get('main', 'modules').split()
superusers = c.get('main', 'super-users').split()
sleep_after_id = c.getfloat('main', 'wait-after-identify')
wait_recv = c.getint('main', 'read-wait')
cmd_char = c.get('main', 'command-char')
ignore = re.compile(c.get('main', 'ignore-re'))

backend = c.get('main', 'backend')
