import q
import api
import config
class trekbot():
    def __init__(self):
        self.blacklist=[]
        self.blconfig=open('trekbot/blacklist','r').readlines()
        for each in self.blconfig:
            self.blacklist.append(each.strip('\r\n'))
        self.whitelist=[]
        self.wlconfig=open('trekbot/whitelist','r').readlines()
        for each in self.wlconfig:
            self.whitelist.append(each.strip('\r\n'))
        del self.blconfig,self.wlconfig
    def go(self,nick,data,channel):
        ldata=data.lower()
        self.superuser=api.checkIfSuperUser(data,config.superusers)
        if self.superuser:
            if ldata.find(':?op')!=-1:
                if ldata.find('?op ')!=-1:
                    nick=ldata[ldata.find('?op')+4:].strip('\r\n')
                q.queue.mode(nick,channel,'+o')
            if ldata.find(':?deop')!=-1:
                if ldata.find('?deop ')!=-1:
                    nick=ldata[ldata.find('?deop ')+6:].strip('\r\n')
                q.queue.mode(nick,channel,'-o')
            elif ldata.find(':?voice')!=-1:
                if ldata.find('?voice ')!=-1:
                    nick=ldata[ldata.find('?voice ')+7:].strip('\r\n')
                q.queue.mode(nick,channel,'+v')
            elif ldata.find(':?devoice')!=-1:
                if ldata.find('?devoice ')!=-1:
                    nick=ldata[ldata.find('?devoice ')+9:].strip('\r\n')
                q.queue.mode(nick,channel,'-v')
            elif ldata.find(':?kick ')!=-1:
                name=ldata[ldata.find('?kick ')+6:].strip('\r\n')
                q.queue.kick(name,channel,'Requested by %s'%nick)
            elif ldata.find('?rehash')!=-1:
                self.__init__()
            #Blacklist
            elif ldata.find(':?blacklist ')!=-1:
                name=data[data.find('?blacklist ')+11:].strip('\r\n')
                if not name in self.blacklist:
                    self.blacklist.append(name)
                    self.write_blacklist()
            elif ldata.find(':?unblacklist ')!=-1:
                name=data[data.find('?unblacklist ')+13:].strip('\r\n')
                if name in self.blacklist:
                    self.blacklist.pop(self.blacklist.index(name))
                    self.write_blacklist()
                else:
                    q.queue.append((nick,'That host is not blacklisted'))
            elif ldata.find(':?listbl')!=-1:
                q.queue.append((nick,str(self.blacklist)))
            #Whitelist
            elif ldata.find(':?whitelist ')!=-1:
                name=data[data.find('?whitelist ')+11:].strip('\r\n')
                if not name in self.whitelist:
                    self.whitelist.append(name)
                    self.write_blacklist()
            elif ldata.find(':?unwhitelistlist ')!=-1:
                name=data[data.find('?unwhitelist ')+13:].strip('\r\n')
                if name in self.blacklist:
                    self.whitelist.pop(self.blacklist.index(name))
                    self.write_whitelist()
                else:
                    q.queue.append((nick,'That host is not whitelisted'))
            elif ldata.find(':?listbl')!=-1:
                q.queue.append((nick,str(self.blacklist)))
            elif ldata.find(':?mode ')!=-1:
                q.queue.mode('',channel,ldata[ldata.find('?mode ')+6:])
            elif data.find(':?echo ')!=-1:
                q.queue.append((channel,data[ldata.find('?echo ')+6:]))
            elif ldata.find(':?ban ')!=-1:
                q.queue.mode(data[data.find('?ban ')+5:],channel,'+b')
            elif ldata.find(':?unban ')!=-1:
                q.queue.mode(data[data.find('?unban ')+7:],channel,'-b')
            elif data.find(':?topic ')!=-1:
                q.queue.raw('TOPIC %s :%s'%(channel,data[data.find('?topic ')+7:]))
            elif data.find(':?nick ')!=-1:
                q.queue.nick(data[data.find('?nick ')+6:])
    def write_blacklist(self):
        self.blconfig=open('trekbot/blacklist','w')
        for each in self.blacklist:
            self.blconfig.write(each+'\n')
    def write_whitelist(self):
        self.wlconfig=open('trekbot/whitelist','w')
        for each in self.whitelist:
            self.wlconfig.write(each+'\n')
    def join(self,nick,channel,ip,user):
        if not ip in self.blacklist:
            if not ip in self.whitelist:
                self.scan(ip,channel,nick)
            else:
                q.queue.mode(nick,channel,'+v')
        else:
            q.queue.kick(nick,channel,'Your on the blacklist, please message a channel op about getting removed from the list')
    def scan(self,ip,channel,nick):
        self.scansafe=1
        try:
            print('Scanning '+ip)
            self.nm=nmap.PortScanner()
            #80, 8080, 1080, 3246
            self.nm.scan(ip,'808,23,1080,110,29505,8080,3246','-T5')
            for each in nm.all_hosts():
                print each+':::'
                lport = nm[each]['tcp'].keys()
                print lport
                if 808 in lport or 23 in lport or 110 in lport or 1080 in lport or 29505 in lport or 80 in lport or 8080 in lports or 3246 in lports:
                    self.scansafe=0
                    print 'DRONE'
            del self.nm
            if self.scansafe:
                queue.mode(nick,channel,'+v')
        except:
            print 'PYTHON NMAP CRASH'