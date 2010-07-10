import q
class WhoBot():
    def go(self,nick,data,channel):
        if nick.lower()=='evilbikcmp' or nick.lower()=='mithos':
            if data.find('?kline ')!=-1:
                nick=data[data.find('?kline ')+7:]
                print nick
                q.queue.raw('WHOIS %s'%nick)
    def code(self,code,data):
        if code=='311':
            self.data=data.split(mynick)[-1].split()
            self.h=self.data[2]
            print 'HOST %s'%self.h
            if self.h.find('webchat/')!=-1:
                self.ident='!'.join(self.data[1:2])
                print 'IDENT: %s'%self.ident
                q.queue.append(('operserv','AKILL ADD !T 6400 %s@%s Spam is offtopic on FOSSnet. Email kline@fossnet.info for help'%(self.ident,self.h)))
            else:
                q.queue.append(('operserv','AKILL ADD !T 6400 *!*@'+self.h+' Spam is offtopic on FOSSnet. Email kline@fossnet.info for help.'))