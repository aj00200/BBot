"""This module contains most of the BBot core functionality, including help system and version output."""

import time

import api
import config
import bbot as BBot

class Module(api.Module):
    # Settings from configuration file
    quit_message = api.get_config_str('main', 'quit-message')
    use_services = api.get_config_bool('main', 'use-services')

    def __init__(self, server):
        super(Module, self).__init__(server)

        self.command_list = []
        self.command_start = ':'+config.cmd_char
        self.cmd_len = len(self.command_start)

        # Let's hook up our commands
        api.hook_command('help', self.help, server)
        api.hook_command('nhelp', self.normal_help, server)
        api.hook_command('shelp', self.su_help, server)
        api.hook_command('version', self.version, server)
        # Superuser commands. Darn, we really need a better auth system
        api.hook_command('join', self.su_join, server, su = True)
        api.hook_command('quit', self.su_quit, server, su = True)
        api.hook_command('part', self.su_part, server, su = True)
        api.hook_command('raw', self.su_raw, server, su = True)
        api.hook_command('load', self.su_load, server, su = True)
        api.hook_command('reload', self.su_reload, server, su = True)
        api.hook_command('py', self.su_py, server, su = True)
        api.hook_command('connect', self.su_connect, server, su = True)

    def privmsg(self, nick, data, channel):
        is_channel = ('#' in channel or '&' in channel) # if message is a pm; local channels not being ignored
                                                        # should be parsed from numeric 005!
        if is_channel: 
            channel = nick
        ldata = data.lower()

        # Version ping
        if '\x01VERSION\x01' in data:
            self.notice(nick, '\x01VERSION BBot Version %s\x01'%BBot.VERSION)

        # Prefix ping - responds with the current command char
        elif '\x01PREFIX\x01' in data:
            self.notice(nick, '\x01PREFIX My current command character is: %s\x01'%config.cmd_char)

    def get_raw(self, t, d):
        '''Parses raw numerics. Handles nick being in use.'''
        if t ==  'code':
            if d[0] ==  '433':
                # Nick is already in use
                self.raw('NICK %s_'%config.nick)
                if use_services:
                    self.msg('NickServ', 'GHOST %s %s'%(config.nick, config.password))
                    time.sleep(api.get_config_float('main', 'wait-after-identify'))
                    self.raw('NICK %s'%config.nick)

    def version(self, nick, channel, param = None):
        '''Sends the version number to the channel; Parameters: None'''
        self.msg(channel, 'BBot Version %s' % BBot.VERSION)

    def help(self, nick, channel, param = None):
        '''Fail to display help; Parameters: None'''
        # We really need to fix this mess with a proper auth system
        self.msg(channel, '%s: please use the command %snhelp for normal help or %sshelp for superuser help' % (nick, config.cmd_char, config.cmd_char))

    def normal_help(self, nick, channel, param = None):
        '''List the commands usable by normal users; Parameters: (optional) command name'''
        if param in api.hooks[self.__address__]:
            self.msg(channel, '%s: %s' % (nick, api.hooks[self.__address__][param].__doc__))
        else:                    
            self.msg(channel, '%s: %s' % (nick, ', '.join(api.get_command_list(self.__address__))))

    def su_help(self, nick, channel, param = None):
        '''List the commands usable by super users; Parameters: (optional) command name'''
        if param in api.su_hooks[self.__address__]:
            self.msg(channel, '%s: %s' % (nick, api.su_hooks[self.__address__][param].__doc__))
        else:
            self.msg(channel, '%s: %s' % (nick, ', '.join(api.get_command_list(self.__address__, su = True))))

    def su_join(self, nick, channel, param = None):
        '''Have BBot join a channel; Parameters: channel'''
        if param:
            self.raw('JOIN %s' % param)
        else:
            self.msg(channel, '%s: You need to specify a channel' % nick)

    def su_raw(self, nick, channel, param = None):
        '''Send a raw message to the server (warning, unexpected results may occur); Parameters: a raw command'''
        if param:
            self.raw(param)
        else:
            self.msg(channel,'%s: you need to specify a raw command' % nick)

    def su_part(self, nick, channel, param = None):
        '''Part a channel; Parameters: a channel name'''
        if param:
            self.raw('PART %s' % param)
        else:
            self.msg(channel, '%s: you need to specify a channel' % nick)

    def su_quit(self, nick, channel, param = None):
        '''Quit; Parameters: an optional quit message'''
        if param:
            self.raw('QUIT :%s' % param)
        else:
            self.raw('QUIT :%s' % self.quit_message)

    def su_load(self, nick, channel, param = None):
        '''Load a module; Parameters: a module name'''
        if api.load_module(self.__address__, param):
            self.notice(channel, '<<Loaded %s>>' % param)
        else:
            self.notice(channel, 'Error loading %s' % param)

    def su_py(self, nick, channel, param = None):
        '''Execute a Python expression; Parameters: a python expression'''
        if not param:
            self.msg(channel, '%s: ...' % nick)
            return
        try:
            ret = str(eval(param))
        except Exception, e:
            ret = '<<Error %s; %s>>' % (type(e), e.args)
        self.msg(channel, ret)

    def su_connect(self, nick, channel, param = None):
        '''Connect to another network; Parameters: address'''
        if param:
            parts = param.split()
            if len(parts) == 1:
                parts.append(config.port)
            self.notice(channel, '<<Connecting to %s>>' % param)
            api.backend.connect(parts[0], int(parts[1]), config.ssl)
        else:
            self.msg(channel, '%s: You need to specify an address' % nick)
net-19b.qe1.d1ih9s.IP
    def su_reload(self, nick, channel, param = None):
        '''Reload a module; Parameters: module'''
        api.backend.connections[self.__address__].reload_module(param)
        self.notice(channel, '<<Reloaded %s>>' % param)
 
