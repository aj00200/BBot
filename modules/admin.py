'''A module which is used to control the bot and make it do actions such as
talking, joining and parting channels, quitting, kicking, mode setting, and
so on. This module also allows for the setup of various access levels which
can give permissions to access the entire bot (with the py command), or can
be used to set limits on what people can do such as controlling channels it
is in. Be careful who you trust or they might just stab you in the back.'''
import api

class Module(api.Module):
    '''A Module for controlling the bot'''
    def __init__(self, address):
        super(Module, self).__init__(address)

        # Hook Superuser Commands
        api.hook_command('join', self.join_cmd, address, su = True)
        api.hook_command('addaccess', self.add_access, address, su = True)

    def join_cmd(self, nick, channel, param = None):
        '''Has the bot join a channel; Parameters: channel name'''
        if param:
            self.join(param)

    def add_access(self, nick, channel, param):
        '''Add access permissions to a host - level 1: join/part access, level 2: raw access, level 3: py access; Parameters: host, access level'''