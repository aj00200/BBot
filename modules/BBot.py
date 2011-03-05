"""This module allows for easy factoid tracking a la Infobot, in addition to
generating URLs for common websites, such as Google SSL, Wikipedia SSL and
aj00200's Knowledge Base. It also allows the admin to execute functions like
loading modules, connecting to other networks and more. Additionally, it can
output important BBot information like its version."""

import re
import time
import thread

import api
import config
import bbot as BBot

try:
    import json
    file = open('database.json')
    dict = json.load(file)
    file.close()
    del file
except:
    print(' * Could not load the factoid file')
    dict = {}
class Module(api.module):
    goog_str = 'https://encrypted.google.com/search?q=%s'
    wiki_str = 'https://secure.wikimedia.org/wikipedia/en/wiki/%s'
    stop_words = [
        ' a ', ' the ', ' was ', ' an '
    ]
    is_words = [
        ' was ', ' are ', ' am '
    ]
    def __init__(self, server):
        api.module.__init__(self, server)
        self.command_list = []
        self.command_start = ':'+config.cmd_char
        self.cmd_len = len(self.command_start)

        # Hook Commands
        api.hook_command('help', self.help, server)
        api.hook_command('nhelp', self.normal_help, server)
        api.hook_command('shelp', self.su_help, server)
        api.hook_command('hit', self.hit, server)
        api.hook_command('version', self.version, server)
        api.hook_command('goog', self.goog, server)
        api.hook_command('wiki', self.wiki, server)
        # Hook Superuser Commands
        api.hook_command('join', self.su_join, server, su = True)
        api.hook_command('writedb', self.su_writedb, server, su = True)
        api.hook_command('raw', self.su_raw, server, su = True)
        api.hook_command('part', self.su_part, server, su = True)
        api.hook_command('add', self.su_add, server, su = True)
        api.hook_command('load', self.su_load, server, su = True)
        api.hook_command('reload', self.su_reload, server, su = True)
        api.hook_command('py', self.su_py, server, su = True)
        api.hook_command('connect', self.su_connect, server, su = True)
        api.hook_command('del', self.su_del, server, su = True)

    def privmsg(self, nick, data, channel):
        if '#' not in channel: # if message is a pm
            channel = nick
        ldata = data.lower()

        # Check if message is a command
        if self.command_start in data:
            cmd = data[data.find(self.command_start)+len(self.command_start):]
            if ' ' in cmd:
                cmd = cmd[:cmd.find(' ')]

            # Superuser Commands
            if api.check_if_super_user(data):
                if ' > ' in data:
                    channel = data[data.find(' > ')+3:]
                    data = data[:data.find(' > ')]
    
            # Normal Commands
            cmd = data[data.find(self.command_start)+self.cmd_len:]
            if ' | ' in cmd:
                nick = cmd[cmd.find(' | ')+3:]
                cmd = cmd[:cmd.find(' | ')]
            self.query(cmd, nick, channel)

        # Check if I've been pinged
        if (' :%s: '%config.nick.lower() in ldata) or (' :%s, '%config.nick.lower() in ldata):
            msg = api.get_message(data).lower()
            q = msg[msg.find(config.nick.lower())+len(config.nick.lower())+2:]
            self.query(q, nick, channel)

        # Answer basic questions
        ldata = ldata.replace('whats', 'what is')
        if re.search('(what|where|who) (is|was|are|am)', ldata):
            for word in self.stop_words:
                ldata = ldata.replace(word, ' ')
            for word in self.is_words:
                ldata = ldata.replace(word, ' is ')
            q = ldata[ldata.find(' is ')+4:].strip('?')
            self.query(q, nick, channel)

        # Version ping
        elif '\x01VERSION\x01' in data:
            self.notice(nick, '\x01VERSION BBot Version %s\x01'%BBot.VERSION)

        # Prefix ping - responds with the current command char
        elif '\x01PREFIX\x01' in data:
            self.notice(nick, '\x01PREFIX My current command character is: %s\x01'%config.cmd_char)

    def get_raw(self, t, d):
        if t ==  'code':
            if d[0] ==  '433':
                # Nick is already in use
                self.raw('NICK %s_'%config.nick)
                if api.get_config_bool('main', 'use-services'):
                    self.msg('NickServ', 'GHOST %s %s'%(config.nick, config.password))
                    time.sleep(api.get_config_float('main', 'wait-after-identify'))
                    self.raw('NICK %s'%config.nick)

    def add_factoid(self, query, nick):
        tmp = query
        try:
            if '<ACTION>'in query[1]:
                tmp[1] = str(tmp[1].replace('<ACTION>', '\x01ACTION ')+'\x01')
            dict[query[0]] = query[1]
            return True
        except IndexError:
            return False

    def query(self, query, nick, channel):
        '''Querys the database for the factoid 'query', and returns its value to the channel if it is found'''
        if query in dict:
            self.msg(channel, str(dict[q].replace('%n', nick)))

    # Single Functions
    def hit(self, nick, channel, param = None):
        '''Causes BBot to punch someone; Parameters: nick to hit'''
        if not param:
            param = nick
        self.msg(channel, '\x01ACTION punches %s\x01' % param)

    def version(self, nick, channel, param = None):
        '''Sends the version number to the channel; Parameters: None'''
        self.msg(channel, 'I am version %s' % BBot.VERSION)

    def goog(self, nick, channel, param = None):
        '''Give a Google URL for a search; Parameters: search query'''
        self.msg(channel, self.goog_str % param.replace(' ','+'))

    def wiki(self, nick, channel, param = None):
        '''Give a Wikipedia URL for a page; Parameters: page name'''
        self.msg(channel, self.wiki_str % param.replace(' ', '_'))

    def help(self, nick, channel, param = None):
        '''Display help options; Parameters: None'''
        self.msg(channel, '%s: please use the command %snhelp for normal help or %snsuhelp for superuser help' %
                 (nick, config.cmd_char, config.cmd_char))

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

    def su_writedb(self, nick, channel, param = None):
        '''Writes the factoids database to the harddrive; Parameters: None'''
        write_dict()
        self.notice(channel, '<<Wrote Database>>')

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

    def su_add(self, nick, channel, param = None):
        '''Add a factoid; Parameters: a factoid name and a factoid body seperated by ":::" - For example, ?add test:::%n: it works!'''
        if channel == config.nick:
            channel = nick
        if param:
            query = param.split(':::')
            if self.add_factoid(query, nick):
                self.notice(channel, '<<Added %s>>' % query)
            else:
                self.msg(channel, '%s: Adding of the factoid failed. Make sure you are using the proper syntax.' % nick)
        else:
            self.msg(channel,'%s: you must specify a factoid to add')

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
            self.notice(channel, '<<Connecting to %s>>' % param)
            api.backend.connect(param, config.port, False)
        else:
            self.msg(channel, '%s: You need to specify an address' % nick)

    def su_reload(self, nick, channel, param = None):
        '''Reload a module; Parameters: module'''
        thread.start_new_thread(api.backend.connections[self.__address__].reload_module, (param, ))
        self.notice(channel, '<<Reloaded %s>>' % param)

    def su_del(self, nick, channel, param = None):
        '''Delete a factoid; Parameters: factoid'''
        if param:
            del_factoid(param)
            self.notice(channel, '<<Deleting %s>>' % param)
        else:
            self.msg(channel, '%s: You must specify a factoid')

def write_dict():
    '''Write all factoids to the hard drive'''
    file = open('database.json', 'w')
    file.write(json.dumps(dict))
    file.close()
def del_factoid(query):
    '''Delete a factoid'''
    if query in dict:
        del dict[query]
def read_dict():
    '''Read factoids from the harddrive keep in RAM'''
    f = open('database.json')
    dict = json.load(f)
    f.close()
