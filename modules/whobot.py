import q
import api
class WhoBot(api.module):
    def __init__(self,server):
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        if api.checkIfSuperUser(data):
            if data.find('?kline ')!=-1:
                nick=data[data.find('?kline ')+7:]
                print nick
                self.raw('WHOIS %s'%nick)
    def get_raw(self,code,data):
        if code=='CODE':
            if data[0]=='311':
                self.data=data[1].split()[3:]
                self.h=self.data[2]
                print 'HOST %s'%self.h
                if self.h.find('webchat/')!=-1:
                    self.ident='!'.join(self.data[1:2])
                    print 'IDENT: %s'%self.ident
                    self.append(('operserv','AKILL ADD %s@%s !T 6400 Spam is offtopic on FOSSnet. Email kline@fossnet.info for help'%(self.ident,self.h)))
                else:
                    self.append(('operserv','AKILL ADD *@'+self.h+' !T 6400 Spam is offtopic on FOSSnet. Email kline@fossnet.info for help.'))
module=WhoBot
