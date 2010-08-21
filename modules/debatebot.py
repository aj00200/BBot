import q
import api
import time
class debatebot(api.module):
    def __init__(self,server):
        self.channel='#debate'
        self.floor=''
        self.last_tal=time.time()
        self.claimed_at=time.time()
        self.hour=21600
        self.minute=60
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        ldata=data.lower()
        if channel==self.channel:
            if ldata.find('?claim')!=-1 and self.floor=='':
                self.claim(nick,channel)
            if ldata.find('?drop')!=-1 and nick==self.floor:
                self.drop(nick)
            elif ldata.find('?debate help')!=-1:
                self.help(nick)
    def loop():
        if time.time()-self.claimed_at>3600:
            self.cutof(self.floor)
    def claim(self,nick,channel):
        self.floor=nick
        self.notice((self.channel,'<<%s is recognized by the channel for a maximum of 1 hour. To propose a topic for debate, say ?propose <topic>, to request entrance into the debate, say ?request>>'%nick))
        self.mode('',self.channel,'+mz')
        self.mode(nick,self.channel,'+v')
        self.claimed_at=time.time()
    def drop(self,nick):
        self.mode(nick,self.channel,'-v')
        self.notice((self.channel,'<<%s has given up control of the floor, to clam it, say ?claim>>'%nick))
        self.floor=''
        self.mode('',self.channel,'-mz')
    def cutof(self,nick):
        self.mode(nick,self,channel,'-v')
        self.notice((self.channel,'<<%s\'s time has expired, the floor can be claimed with ?claim>>'))
        self.floor=''
        self.mode('',self.channel,'-v')
    def help(self,nick):
        self.append((nick,'?claim, ?drop, ?yeild -NOT ALL COMMANDS WORK YET'))
module=debatebot
