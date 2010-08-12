import q
import api
import time
import config
import thread
import colorz
import re
proxyscan=1
class blockbot(api.module):
    def __init__(self,server):
        self.ignore_users_on_su_list=1#Don't kick users if they are on the superusers list
        self.jlist={}
        self.config=open('blockbot-config','r')
        self.findlist=self.config.readline().split('spam-strings: ')[1].split('#')[0].split('^^^@@@^^^')
        self.proxyscan=0
        if self.config.readline().lower().split('#')[0].find('yes')!=-1:
            self.proxyscan=1
            proxyscan=1
        if self.proxyscan==1:
            import nmap #Can be found at: http://xael.org/norman/python/python-nmap/
        self.line=self.config.readline()
        self.wait=float(self.line.split('-speed: ')[-1].split(' #')[0])
        self.config.close()
        self.repeatlimit=3
        self.repeat_time=2
        self.repeat_1word=4
        self.msglist=[]
        self.lastnot=('BBot',time.time(),'sdkljfls')
        api.module.__init__(self,server)
    def join(self,nick,channel,ip,user):
        #webchat=(str(blockbotlib.hex2dec('0x'+str(user[1:3])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[3:5])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[5:7])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[7:9]))))
        if channel[1:] not in self.jlist:
            self.jlist[channel[1:]]=[]
        self.jlist[channel[1:]].append(nick)
        if proxyscan:
            thread.start_new_thread(self.scan, (ip,channel,nick))
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
                    print colorz.encode('DRONE','yellow')
            del self.nm
            if self.scansafe:
                self.mode(nick,channel,'+v')
        except:
            print colorz.encode('PYTHON NMAP CRASH','red')
    def go(self,nick,data,channel):
        self.ldata=data.lower()
        if self.ignore_users_on_su_list:
            self.superuser=api.checkIfSuperUser(data,config.superusers)
        if self.superuser:
            if self.ldata.find(':?;')!=-1:
                self.findlist.append(data[data.find(':?; ')+4:].lower())
            elif self.ldata.find(':?faster')!=-1:
                print(colorz.encode('FASTER','cayn'))
                self.wait=self.wait/2
            elif self.ldata.find(':?slower')!=-1:
                print(colorz.encode('SLOWER','cayn'))
                self.wait=self.wait*2
            elif self.ldata.find(':?setspeed ')!=-1:
                self.wait=float(data.split('?setspeed ')[-1][0:-2])
            elif self.ldata.find(':?rehash')!=-1:
                self.__init__(self.__server__)
            elif self.ldata.find(':?protect')!=-1:
                self.mode('',channel,'+mz')
            elif self.ldata.find(':?kl')!=-1:
                if self.ldata.find('?kl ')!=-1:
                    self.t=self.ldata.split('?kl ')[-1][0:-2]
                    self.t=int(self.t)
                    try:
                        for each in range(t):
                            self.kick(self.jlist[channel[1:]].pop(),channel)
                    except:
                        self.append((nick,'Kicking that many people has caused an error!'))
        elif not self.superuser:
            self.checkforspam(nick,data,channel)
    def checkforspam(self,nick,data,channel):
        self.msglist.insert(0,(nick,time.time(),data))
        if len(self.msglist)>5:
            self.msglist.pop()
        ident=data.split(' PRIVMSG ')[0].split('@')[0][1:]
        ldata=data.lower()
        msg=ldata[ldata.find(' :')+2:]
        for each in self.findlist:
            if re.search(each,ldata):
                self.mode('*!*@%s'%api.getHost(data),channel,'+b')
                self.kick(nick,channel,'You have matched a spam string and have been banned from the channel, if you think this is a mistake, contact a channel op about being unbaned')
        try:
            if self.msglist[0][0]==self.msglist[1][0]==self.msglist[2][0]:
                if (self.msglist[0][1]-self.msglist[2][1])<self.wait:
                    self.kick(nick,channel,'No Flooding! If you keep doing this, you will be banned.')
                if msg.split()>1:
                    if (self.msglist[0][2]==self.msglist[1][2]==self.msglist[2][2]) and (self.msglist[0][1]-self.msglist[1][1]<self.repeat_time):
                        self.kick(nick,channel,'Please do not repeat!')
                        self.mode('*!*@%s'%api.getHost(data),channel,'+b')
        except IndexError:
            pass
    def notice(self,nick,channel,data):
        ldata=data.lower()
        self.olastnot=(self.lastnot[0:])
        self.lastnot=(nick,time.time())
        if self.olastnot[0]==self.lastnot[0]:
            if (self.lastnot[1]-self.olastnot[1])<self.wait:
                self.kick(nick,channel,'Please do not use the notice command so much')
        for each in self.findlist:
            if ldata.find(each)!=-1:
                self.kick(nick,channel)
module=blockbot
