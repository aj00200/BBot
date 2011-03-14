'''An asynchat backend for BBot'''
import socket, asynchat
import re, time, ssl, traceback

import bbot, config
import api

connections = {}
class Connection(asynchat.async_chat):
    re001 = re.compile('\.* 001')
    def __init__(self, address, port, use_ssl):
        # Setup Asynchat
        asynchat.async_chat.__init__(self)

        self.data = ''
        self.modules = []
        self.ssl = use_ssl
        self.__address__ = address
        self.set_terminator('\r\n')

        # Setup Command Hooks
        api.hooks[address] = {}
        api.su_hooks[address] = {}

        # Setup Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if use_ssl:
            try:
                self.ssl_sock = ssl.wrap_socket(self.sock)
                self.ssl_sock.connect((address, port))
                self.set_socket(self.ssl_sock)
            except ssl.SSLError, error:
                print('\x1B[31m')
                print('There has been an SSL error while connecting to the server')
                print('Please make sure you are using the proper port')
                print('If you need help, join #bbot on irc.fossnet.info (port 6667; ssl: 6670)')
                print('\x1B[m\x1B[m')
                raise ssl.SSLError(error)
            except socket.error, error:
                print('There was an error connecting to %s' % address)
                return
        else:
            try:
                self.sock.connect((address, port))
            except socket.error, error:
                print('There was an error connecting to %s' % address)
                return
            self.set_socket(self.sock)

    def load_modules(self):
        '''Load all the modules which are set in the config'''
        for module in config.modules:
            self.load_module(module)

    def handle_error(self):
        traceback.print_exc()

    def load_module(self, module):
        try:
            self.modules.append(getattr(__import__('modules.'+module), module).Module(self.__address__))
            return True
        except ImportError:
            try:
                self.modules.append(getattr(__import__('usermodules.'+module), module).Module(self.__address__))
                return True
            except ImportError:
                print(' * ImportError loading %s' % module)
                return False

    def unload_module(self, module):
        for mod in self.modules:
            if (str(type(mod)) ==  "<class 'modules.%s.Module'>" % module or str(type(mod)) == "<class 'usermodules.%s.Module'>" % module):
                print ' * Removing module %s for network %s' % (module, self.__address__)
                mod.destroy()
                self.modules.pop(self.modules.index(mod))

    def reload_module(self, module):
        self.unload_module(module)
        try:
            self.modules.append(reload(getattr(__import__('modules.'+module), module)).Module(self.__address__))
        except ImportError, error:
            reload(getattr(__import__('usermodules.'+module), module))
        time.sleep(2)
        self.load_module(module)

    def handle_connect(self):
        print(' * Connected')
        self.push('NICK %s\r\nUSER %s %s %s :%s\r\n' % (config.nick, config.nick, config.nick, config.nick, config.nick))

    def get_data(self):
        ret = self.data
        self.data = ''
        return ret

    def found_terminator(self):
        data = self.get_data()
        if re.search(config.ignore, data.lower()):
            return
        command = data.split(' ', 2)[1]
        print('Recv: %s' % data)
        if data[:4] == 'PING':
            self.push('PONG %s\r\n' % data[5:])

        elif command ==  'PRIVMSG':
            nick = data[1:data.find('!')]
            channel = data[data.find('MSG')+4:data.find(' :')]
            for module in self.modules:
                module.privmsg(nick, data, channel)
            # Command Hooks
            if channel == config.nick:
                channel = nick
            if ' :%s' % config.cmd_char in data:
                prm = None
                msg = api.get_message(data)
                cmd = msg[msg.find(config.cmd_char)+1:]
                if ' ' in cmd:
                    prm = cmd[cmd.find(' ')+1:]
                    cmd = cmd[:cmd.find(' ')]

                if cmd in api.hooks[self.__address__]:
                    api.hooks[self.__address__][cmd](nick, channel, prm)
                # Superuser Hooks
                if api.check_if_super_user(data):
                    if cmd in api.su_hooks[self.__address__]:
                        api.su_hooks[self.__address__][cmd](nick, channel, prm)

        elif command ==  'NOTICE':
            nick = data[1:data.find('!')]
            channel = data[data.find('ICE')+4:data.find(' :')]
            for module in self.modules:
                module.get_notice(nick, data, channel)

        elif command ==  'JOIN':
            nick = data.split('!')[0][1:]
            if nick.find('#') == -1:
                channel = data[data.find(' :#')+2:]
                host = data[data.find('@')+1:data.find(' JOIN ')]
                user1 = data[data.find('!'):data.find('@')]
                user = user1.replace("!", "")
                for module in self.modules:
                    module.get_join(nick, user, host, channel)

        elif re.search(self.re001, data):
            if bbot.api.get_config_bool('main', 'use-services'):
                self.push('PRIVMSG NickServ :IDENTIFY %s %s\r\n'%(config.username, config.password))
                time.sleep(config.sleep_after_id)
            for channel in config.autojoin:
                self.push('JOIN %s\r\n'%channel)

        elif re.search('[0-9]+ *' + config.nick, data):
            code = data.split()[1]
            for module in self.modules:
                module.get_raw('code', (code, data))

    def collect_incoming_data(self, data):
        self.data += data

def connect(address, port = 6667, use_ssl = False):
    '''Connect to an IRC network
    address - The network address of the IRC network
    port - On optional argument that specifies the port to connect on
    ssl - A boolean argument specifying wether or not to use SSL'''
    connections[address] = Connection(address, port, use_ssl)
    connections[address].load_modules()
