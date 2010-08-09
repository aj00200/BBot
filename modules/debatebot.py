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
                self.floor=nick
                self.notice((self.channel,'<<%s is recognized by the channel for a maximum of 1 hour. To propose a topic for debate, say ?propose <topic>, to request entrance into the debate, say ?request>>'%nick))
                self.mode('',self.channel,'+mz')
                self.mode(nick,self.channel,'+v')
                self.claimed_at=time.time()
            if ldata.find('?drop')!=-1 and nick==self.floor:
                self.mode(nick,self.channel,'-v')
                self.notice((self.channel,'<<%s has given up control of the floor, to clam it, say ?claim>>'%nick))
                self.floor=''
                self.mode('',self.channel,'-mz')
module=debatebot
