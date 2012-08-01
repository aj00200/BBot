'''An asynchat backend for BBot.'''
import socket
import asynchat
import asyncore
import traceback
import time
import ssl
import re

import bbot
import config
import api

connections = {}

class Connection(asynchat.async_chat): 
    '''Class containing the connection to each server and modules.'''
    re001 = re.compile('\.* 001')
    def __init__(self, address, port, use_ssl):
        # Setup Asynchat
        asynchat.async_chat.__init__(self)

        self.data = b''
        self.modules = {}
        self.ssl = use_ssl
        self.__address__ = address
        self.netname = address.replace('irc.', '')
        self.set_terminator(b'\r\n')

        # Setup Command Hooks
        api.hooks[address] = {}
        api.su_hooks[address] = {}
        api.mode_hooks[address] = []

        # Setup Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if use_ssl:
            try:
                self.ssl_sock = ssl.wrap_socket(self.sock)
                self.ssl_sock.connect((address, port))
                self.set_socket(self.ssl_sock)
            except ssl.SSLError as error:
                print('\x1B[31m')
                print('There has been a SSL error connecting to the server')
                print('Please make sure you are using the proper port')
                print('For help, try #bbot on irc.ospnet.org (ssl: 6697)')
                print('\x1B[m\x1B[m')
                raise ssl.SSLError(error)
            except socket.error as error:
                self.output('There was an error connecting')
                return
        else:
            try:
                self.sock.connect((address, port))
            except socket.error as error:
                self.output('There was an error connecting')
                return
            self.set_socket(self.sock)

    def load_modules(self):
        '''Load all the modules which are set in the config.'''
        for module in config.modules:
            self.load_module(module)

    def handle_error(self):
        '''Print a traceback when an error happens.'''
        traceback.print_exc()

    def load_module(self, module):
        '''Load a module for the network.'''
        try:
            self.modules[module] = getattr(__import__('modules.'+module), module).Module(self.__address__)
            return True
        except ImportError:
            try:
                self.modules[module] = getattr(__import__('usermodules.'+module), module).Module(self.__address__)
                return True
            except ImportError:
                self.output('ImportError loading %s' % module)
                return False

    def unload_module(self, module):
        '''Unload a module for the network.'''
        if module in self.modules:
            self.output('Removing module %s' % module)
            self.modules[module].destroy()
            del self.modules[module]

    def reload_module(self, module):
        '''Reload a module by calling the unload_module method followed
        by a reload of the file and finally running the load_module
        method to reload the module for the network.
        '''
        self.unload_module(module)
        try:
            reload(getattr(__import__('modules.'+module), module)).Module(self.__address__)
        except ImportError as error:
            reload(getattr(__import__('usermodules.'+module), module))
        self.load_module(module)

    def handle_connect(self):
        self.output('Connected')
        mode_numeric = 0
        umodes = api.get_config_str("main", "umodes") or ''
        if 'w' in umodes:
            mode_numeric += 1 << 2 # Set bit 2 (rfc2812#section-3.1.3)
        if 'i' in umodes:
            mode_numeric += 1 << 3 # Set bit 3 (rfc2812#section-3.1.3)
        self.push('NICK %s\r\nUSER %s %d * :%s\r\n' % 
                  (config.nick, config.ident, mode_numeric, config.ircname))

    def get_data(self):
        ret = self.data
        self.data = b''
        return ret

    def push(self, data):
        data = data.encode('utf8')
        asynchat.async_chat.push(self, data)

    def found_terminator(self):
        data = self.get_data().decode('utf8')
        # Check if we should ignore this message
        if re.search(config.ignore, data.lower()):
            return

        self.output('R%s' % data)

        # Take an accion based on the command
        command = data.split(' ', 2)[1]
        if data[:4] == 'PING':
            self.push('PONG %s\r\n' % data[5:])

        elif command ==  'PRIVMSG':
            nick = data[1:data.find('!')]
            channel = data[data.find(' PRIVMSG ')+9:data.find(' :')]
            for module in self.modules:
                self.modules[module].privmsg(nick, data, channel)
            # Command Hooks
            if channel == config.nick:
                channel = nick
            if ' :%s' % config.cmd_char in data:
                prm = None
                msg = api.get_message(data)
                cmd = msg[msg.find(config.cmd_char)+1:]
                user = User(nick)
                user.ident = api.get_ident(data)
                user.host = api.get_host(data)
                if ' ' in cmd:
                    prm = cmd[cmd.find(' ')+1:]
                    cmd = cmd[:cmd.find(' ')]

                if cmd in api.hooks[self.__address__]:
                    api.hooks[self.__address__][cmd](user, channel, prm)
                # Superuser Hooks
                if api.check_if_super_user(data):
                    if cmd in api.su_hooks[self.__address__]:
                        api.su_hooks[self.__address__][cmd](user, channel, prm)

        elif command ==  'NOTICE':
            nick = data[1:data.find('!')]
            channel = data[data.find(' NOTICE ')+8:data.find(' :')]
            print('channel: "%s"' % channel)
            for module in self.modules:
                self.modules[module].get_notice(nick, data, channel)

        elif command ==  'JOIN':
            nick = data.split('!')[0][1:]
            if nick.find('#') == -1:
                channel = data[data.find(' :#')+2:]
                host = data[data.find('@')+1:data.find(' JOIN ')]
                user1 = data[data.find('!'):data.find('@')]
                user = user1.replace("!", "")
                for module in self.modules:
                    self.modules[module].get_join(nick, user, host, channel)

        elif command == 'MODE':
            nick = api.get_nick(data)
            channel = data[data.find(' MODE ')+6:]
            mode = channel[channel.find(' ')+1:]
            channel = channel[:channel.find(' ')]
            for hook in api.mode_hooks[self.__address__]:
                hook(nick, channel, mode)

        elif re.search('[0-9]+ *' + config.nick, data):
            code = data.split()[1]
            for module in self.modules:
                self.modules[module].get_raw('CODE', (code, data))
            
            if code == '001':
                if bbot.api.get_config_bool('main', 'use-services'):
                    self.push('PRIVMSG NickServ :IDENTIFY %s %s\r\n' %
                                (config.username, config.password))
                    time.sleep(config.sleep_after_id)
                for channel in config.autojoin:
                    self.push('JOIN %s\r\n' % channel)

    def collect_incoming_data(self, data):
        self.data += data
        
    def output(self, message):
        '''Print a message and display the network name.'''
        print('[%s] %s' % (self.netname, message))

def connect(address, port = 6667, use_ssl = False):
    '''Connect to an IRC network:
    address - The network address of the IRC network
    port - On optional argument that specifies the port to connect on
    ssl - A boolean argument specifying wether or not to use SSL
    '''
    print('[*] Connecting to %s:%s; SSL: %s' % (address, port, use_ssl))
    connections[address] = Connection(address, port, use_ssl)
    connections[address].load_modules()

class User(str):
    '''An object which stores data on a user. It subclasses the str
    object to maintain backwards compatibility.
    '''
    pass

def loop():
    '''Start the backend loop.'''
    asyncore.loop()
