import q
import api
class module(api.module):
    def privmsg(self,nick,data,channel):
        self.msg(channel,'<%s> %s'%(nick,data))
