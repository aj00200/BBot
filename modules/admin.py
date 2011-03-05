import re, api, time, config, thread, colorz, sqlite3
reportchan = "#mithos-ctl"
class Module(api.module):
    '''A Module for controlling the bot'''
    def __init__(self, address):
        api.module.__init__(self, address)

        # Hook Superuser Commands
        api.hook_command('join', self.join_cmd, address, su = True)
        api.hook_command('addaccess', self.add_access, address, su = True)
    def join_cmd(self, nick, channel, param = None):
        '''Has the bot join a channel; Parameters: channel name'''
        if param:
            self.join(channel)

    def add_access(self, nick, channel, param):
        '''Add access permissions to a host - level 1: join/part access, level 2: raw access, level 3: py access; Parameters: host, access level'''
        
