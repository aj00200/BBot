"""This module allows for easy factoid tracking a la Infobot, in addition to
generating URLs for common websites, such as Google SSL and Wikipedia SSL and
hitting people over IRC."""

import re
import time
import thread

import api
import config
import bbot as BBot

try:
    import json
    file = open(config.PATH + 'database.json')
    dict = json.load(file)
    file.close()
    del file
except:
    print(' * Could not load the factoid file')
    dict = {}

class Module(api.Module):
    # Setup module constants
    goog_str = 'https://encrypted.google.com/search?q=%s'
    wiki_str = 'https://secure.wikimedia.org/wikipedia/en/wiki/%s'
    stop_words = [
        ' a ', ' the ', ' was ', ' an '
    ]
    is_words = [
        ' was ', ' are ', ' am '
    ]

    def __init__(self, server):
        super(Module, self).__init__(server)

        self.command_list = []
        self.command_start = ':'+config.cmd_char
        self.cmd_len = len(self.command_start)

        # Hook Commands
        api.hook_command('hit', self.hit, server)
        api.hook_command('version', self.version, server)
        api.hook_command('goog', self.goog, server)
        api.hook_command('wiki', self.wiki, server)
        # Hook Superuser Commands
        api.hook_command('writedb', self.su_writedb, server, su = True)
        api.hook_command('add', self.su_add, server, su = True)
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
            self.msg(channel, str(dict[query].replace('%n', nick)))

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
        if param:
            self.msg(channel, self.goog_str % paaram.replace(' ','+'))

    def wiki(self, nick, channel, param = None):
        '''Give a Wikipedia URL for a page; Parameters: page name'''
        if param:
            self.msg(channel, self.wiki_str % param.replace(' ', '_'))

    def su_writedb(self, nick, channel, param = None):
        '''Writes the factoids database to the harddrive; Parameters: None'''
        write_dict()
        self.notice(channel, '<<Wrote Database>>')

    def su_add(self, nick, channel, param = None):
        '''Add a factoid; Parameters: a factoid name and a factoid body seperated by ":::" - For example, ?add test:::%n: it works!'''
        if param:
            query = param.split(':::', 1)
            if self.add_factoid(query, nick):
                self.notice(channel, '<<Added %s>>' % query)
            else:
                self.msg(channel, '%s: Adding of the factoid failed. Make sure you are using the proper syntax.' % nick)
        else:
            self.msg(channel,'%s: you must specify a factoid to add' % nick)

    def su_del(self, nick, channel, param = None):
        '''Delete a factoid; Parameters: factoid'''
        if param:
            del_factoid(param)
            self.notice(channel, '<<Deleting %s>>' % param)
        else:
            self.msg(channel, '%s: You must specify a factoid')

def write_dict():
    '''Write all factoids to the hard drive'''
    file = open(config.PATH + 'database.json', 'w')
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
