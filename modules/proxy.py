import q
import api
class proxy(api.module):
    chan='#bbot'
    net1='irc.fossnet.info'
    net2='irc.freenode.net'
    def __init__(self,server):
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        if channel==self.chan:
            if self.__server__==self.net1:
                self.to=self.net2
            elif self.__server__==self.net2:
                self.to=self.net1
            else:
                self.to=self.net1
            try:
                q.append(self.to,(channel,'<%s> %s'%(nick,data[data.find(' :')+2:])))
            except Exception:
                pass
module=proxy
