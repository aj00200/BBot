import q,api,config
class module(api.module):
    commands=['op','deop','kick','ban','unban','nick','echo','mode','voice','devoice','blacklist','unblacklist','listbl','whitelist','unwhitelist','topic']
    def __init__(self,server=config.network):
        self.blacklist=[]
        self.blconfig=open('trekbot/blacklist','r').readlines()
        for each in self.blconfig:
            self.blacklist.append(each.strip('\r\n'))
        self.whitelist=[]
        self.wlconfig=open('trekbot/whitelist','r').readlines()
        for each in self.wlconfig:
            self.whitelist.append(each.strip('\r\n'))
        del self.blconfig,self.wlconfig
        self.proxyscan=api.getConfigBool('trekbot','proxy-scan')
        api.module.__init__(self,server)
    def privmsg(self,nick,data,channel):
        ldata=data.lower()
        self.superuser=api.checkIfSuperUser(data,config.superusers)
        if self.superuser:
            if ':?op' in ldata:
                if '?op ' in ldata:
                    nick=ldata[ldata.find('?op')+4:]
                self.mode(nick,channel,'+o')
            elif ':?deop' in ldata:
                if '?deop ' in ldata:
                    nick=ldata[ldata.find('?deop ')+6:]
                self.mode(nick,channel,'-o')
            elif ':?voice' in ldata:
                if '?voice ' in ldata:
                    nick=ldata[ldata.find('?voice ')+7:]
                self.mode(nick,channel,'+v')
            elif ':?devoice ' in ldata:
                nick=ldata[ldata.find('?devoice ')+9:]
                self.mode(nick,channel,'-v')
            elif ':?quiet ' in ldata:
                nick=ldata[ldata.find('?quiet ')+7:]
                self.mode(nick,channel,'+q')
            elif ':?kick ' in ldata:
                name=ldata[ldata.find('?kick ')+6:]
                self.kick(name,channel,'Requested by %s'%nick)
            elif ldata.find('?rehash')!=-1:
                self.__init__()
            #Blacklist
            elif ':?blacklist ' in data:
                name=data[data.find('?blacklist ')+11:]
                if not name in self.blacklist:
                    self.blacklist.append(name)
                    self.write_blacklist()
            elif ':?unblacklist ' in ldata:
                name=data[data.find('?unblacklist ')+13:]
                if name in self.blacklist:
                    self.blacklist.pop(self.blacklist.index(name))
                    self.write_blacklist()
                else:
                    self.msg(nick,'That host is not blacklisted')
            elif ':?listbl' in ldata:
                self.msg(nick,str(self.blacklist))
            elif ':?whitelist ' in ldata:
                name=data[data.find('?whitelist ')+11:]
                if not name in self.whitelist:
                    self.whitelist.append(name)
                    self.write_blacklist()
            elif ':?unwhitelistlist ' in ldata:
                name=data[data.find('?unwhitelist ')+13:]
                if name in self.blacklist:
                    self.whitelist.pop(self.blacklist.index(name))
                    self.write_whitelist()
                else:
                    self.msg(nick,'That host is not whitelisted')
            elif ':?listbl' in ldata:
                self.msg(nick,str(self.blacklist))
            elif ':?mode ' in ldata:
                self.mode('',channel,ldata[ldata.find('?mode ')+6:])
            elif ':?echo ' in ldata:
                self.msg(channel,data[ldata.find('?echo ')+6:])
            elif ':?ban ' in ldata:
                self.mode(data[data.find('?ban ')+5:],channel,'+b')
            elif ':?unban ' in ldata:
                self.mode(data[data.find('?unban ')+7:],channel,'-b')
            elif ':?topic ' in ldata:
                self.raw('TOPIC %s :%s'%(channel,data[data.find('?topic ')+7:]))
            elif ':?nick ' in ldata:
                self.nick(data[data.find('?nick ')+6:])
    def write_blacklist(self):
        self.blconfig=open('trekbot/blacklist','w')
        for each in self.blacklist:
            self.blconfig.write(each+'\n')
    def write_whitelist(self):
        self.wlconfig=open('trekbot/whitelist','w')
        for each in self.whitelist:
            self.wlconfig.write(each+'\n')
    def get_join(self,nick,channel,ip,user):
        print "GOT JOIN"
        
        if not ip in self.blacklist:
            if not ip in self.whitelist:
                if self.proxyscan:
                    self.scan(ip,channel,nick)
            else:
                self.mode(nick,channel,'+v')
        else:
            self.kick(nick,channel,'You are on the blacklist, please message a channel op about getting removed from the list')
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
                self.mode(nick,channel,'+v')
        except:
            print 'PYTHON NMAP CRASH'
