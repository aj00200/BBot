'''An API for BBot modules to use. Just `import api` and subclass api.Module.
Other functions that are shared across modules are present as well.
'''
import config
backend = getattr(__import__('backends.%s' % config.backend), config.backend)

def get_config_str(cat, name):
    '''Get a string out of the bot's configuration file'''
    return config.c.get(cat, name)

def get_config_int(cat, name):
    '''Get an integer out of the bot's configuration file'''
    return config.c.getint(cat, name)

def get_config_float(cat, name):
    '''Get a floating point number out of the bot's configuration file'''
    return config.c.getfloat(cat, name)

def get_config_bool(cat, name):
    '''Get a boolean value out of the bot's configuration file'''
    return config.c.getboolean(cat, name)

def host_in_list(host, host_list):
    '''Tells you if the host of the person who sent the message that is
    pased as the first arg is in the list of hosts which is the second arg
    '''
    for each in host_list:
        if host.find(each)!= -1:
            return True
    else:
        return False

def check_if_super_user(host, superusers = config.superusers):
    '''Check if the person who sent the current message is a superuser'''
    return host_in_list(host, superusers)

def load_module(server, module):
    '''Tell the backend to load a module for a connection'''
    return backend.connections[server].load_module(module)

def connected_to(server):
    '''Returns True if the bot is connected to server.'''
    if server in backend.connections:
        return True
    return False

# Hooks
hooks = {}
su_hooks = {}
def hook_command(name, callback, server, su = False):
    '''Hook a command for use by the backend, using this when possible will
    increase the speed of the bot and your module
    '''
    if (server not in hooks):
        return False
    try:
        if not su:
            hooks[server][name] = callback
            return True
        else:
            su_hooks[server][name] = callback
            return True
    except IndexError:
        return False

def get_command_list(address, su = False):
    '''Get a list of commands which are hooked for a specfic server'''
    try:
        if not su:
            return list(hooks[address])
        else:
            return list(su_hooks[address])
    except IndexError:
        return 'There was an error processing your request'

mode_hooks = {}
def hook_mode(callback, server):
    '''Hook mode changes and call the callback function each time it changes'''
    if not connected_to(server):
        return False
    if server in mode_hooks:
        mode_hooks[server].append(callback)
    else:
        mode_hooks[server] = [callback]
    return True

def unhook_mode(server, callback):
    '''Unhook a mode callback.'''
    try:
        mode_hooks[server].remove(callback)
        return True
    except IndexError:
        return False

# Base Module
class Module(object):
    '''Base class that all modules should use to maintain decent
    compatibility with future versions of the API
    '''
    def __init__(self, address):
        self.__address__ = address
        self.connection = backend.connections[address]

    def destroy(self):
        '''This is called when the module is unloaded, or possibly when the
        bot is shut down.'''
        pass
    
    # Receive
    def privmsg(self, nick, data, channel):
        '''Called every time a PRIVMSG is recieved.
        nick: the nickname of the person sending the message
        data: the raw data recieced (without the line ending)
        channel: the channel the message was recieved in'''
        pass
    def get_notice(self, nick, data, channel):
        '''Called every time a notice is recieved'''
        pass
    def get_join(self, nick, user, host, channel):
        '''Called every time someone joins a channel the bot is in'''
        pass
    def get_raw(self, msg_type, params):
        '''Called every time non-common data is recieved like mode changes:
        msg_type is set to 'CODE' when messages that corespond to a numberic code are recieved
        msg_type is set to 'MODE' when a mode is changed'''
        pass
    
    # Send
    def msg(self, channel, data = ' '):
        '''Send a message, data, to channel
        Example: self.msg('#bbot', 'Hello world!')'''
        self.raw('PRIVMSG %s :%s\r\n' % (channel, data))
    def notice(self, channel, data):
        '''Send a notice to a channel
        Example: self.notice('#bbot', 'Please do not abuse the bots')'''
        self.raw('NOTICE %s :%s\r\n' % (channel, data))
    def join(self, channel):
        '''Have BBot join a channel:
        Example: self.join('#bbot')'''
        self.raw('JOIN %s\r\n'%channel)
    def part(self, channel, message = 'BBot the IRC Bot'):
        '''Have BBot part a channel
        Example: self.part('#bbot')'''
        self.raw('PART %s :%s\r\n' % (channel, message))
    def kick(self, nick, channel, message = ''):
        '''Kick a person out of a channel
        Example: self.kick('spammer', '#bbot', 'Spam is forbidden')'''
        self.raw('KICK '+channel+' '+nick+' :'+message+'\r\n')
    def mode(self, nick, channel, mode):
        '''Set the mode, mode, on nick in channel.
        If you want to set a normal channel mode, set nick to ''.'''
        self.raw('MODE '+channel+' '+mode+' '+nick+'\r\n')
    def raw(self, data):
        '''Send raw data to the server
        Example: self.raw('PRIVMSG #bbot :This is a raw message')
        Note: the line ending is not required'''
        self.connection.push('%s\r\n' % (data))
        print('Send: %s' % data)
        
    # extra
    def output(self, message):
        '''Print a message with the server name prefix.'''
        self.connection.output(message)
