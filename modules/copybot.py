"""This provides a bridge between private messages and channels, copying raw text received via /msg to a
channel."""

import q
import api
class module(api.module):
    def privmsg(self,nick,data,channel):
        self.msg(channel,'<%s> %s'%(nick,data))
