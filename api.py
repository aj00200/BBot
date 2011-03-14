import config
backend = getattr(__import__('backends.%s'%config.backend), config.backend)
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
def get_host(data):
    '''Returns the hostname (IP address) of the person who
    sent the message passed to the variable data'''
    return data[data.find('@')+1:data.find(' ')]
def get_nick(data):
    '''Returns the nick of the person who sent the message passed as data'''
    return data[1:data.find('!')]
def get_ident(data):
    '''Returns the ident of the person who sent the message passed as data'''
    return data[data.find('!')+1:data.find('@')]
def get_message(data):
    '''Returns the actual message that was sent'''
    return data[data.find(' :')+2:]
def host_in_list(data, list):
    '''Tells you if the host of the person who sent the message that is
    pased as the first arg is in the list of hosts which is the second arg'''
    host = get_host(data)
    for su in list:
        if host.find(su)!= -1:
            return True
    else:
        return False
def check_if_super_user(data, superusers = config.superusers):
    '''Check if the person who sent the current message is a superuser'''
    return host_in_list(data, superusers)
def load_module(server, module):
    '''Tell the backend to load a module for a connection'''
    return backend.connections[server].load_module(module)

# Hooks
hooks = {}
su_hooks = {}
def hook_command(name, callback, server, su = False):
    '''Hook a command for use by the backend, using this when possible will increase the speed of the bot and your module'''
    if (server not in hooks):
        return False
    try:
        if not su:
            hooks[server][name] = callback
            return True
        else:
            su_hooks[server][name] = callback
    except:
        return False

def get_command_list(address, su = False):
    try:
        if not su:
            return list(hooks[address])
        else:
            return list(su_hooks[address])
    except:
        return 'There was an error processing your request'

# Base Module
class Module(object):
    '''Base class that all modules should use to maintain best compatibility
    with future versions of the API'''
    # Setup and Destroy the module
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
    def get_raw(self, type, params):
        '''Called every time non-common data is recieved like mode changes:
        type is set to 'CODE' when messages that corespond to a numberic code are recieved
        type is set to 'MODE' when a mode is changed'''
        pass
    # Send
    def msg(self, channel, data = ' '):
        '''Send a message, data, to channel
        Example: self.msg('#bbot', 'Hello world!')'''
        self.raw('PRIVMSG %s :%s\r\n'%(channel, data))
    def notice(self, channel, data):
        '''Send a notice to a channel
        Example: self.notice('#bbot', 'Please do not abuse the bots')'''
        self.raw('NOTICE %s :%s\r\n'%(channel, data))
    def join(self, channel):
        '''Have BBot join a channel:
        Example: self.join('#bbot')'''
        self.raw('JOIN %s\r\n'%channel)
    def part(self, channel, message = 'BBot the IRC Bot'):
        '''Have BBot part a channel
        Example: self.part('#bbot')'''
        self.raw('PART %s :%s\r\n'%(channel, message))
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
        self.connection.push('%s\r\n'%(data))
        print 'Send: %s' % data
