"""This module allows for easy factoid tracking a la Infobot, in addition to
generating URLs for common websites, such as Google SSL and Wikipedia SSL and
hitting people over IRC."""

import re
import time
import thread

import api
import config
import bbot as BBot

class Module(api.Module):
    # Setup module constants
    goog_str = 'https://encrypted.google.com/search?q=%s'
    wiki_str = 'https://secure.wikimedia.org/wikipedia/en/wiki/%s'

    def __init__(self, address):
        super(Module, self).__init__(address)

        # Hook Commands
        api.hook_command('version', self.version, address)
        api.hook_command('goog', self.goog, address)
        api.hook_command('wiki', self.wiki, address)

    # Single Functions
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

