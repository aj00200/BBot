'''This module causes to bot to copy everyone else'''
import api

class Module(api.module):
    def privmsg(self, nick, data, channel):
        self.msg(channel, '<%s> %s'%(nick, data))
