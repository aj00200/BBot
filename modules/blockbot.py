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
        self.nicklists={}
        self.hilight_limit=3
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
    def get_join(self,nick,channel,ip,user):
        '''Add user to nicklist, and preform optional proxy scan'''
        #webchat=(str(blockbotlib.hex2dec('0x'+str(user[1:3])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[3:5])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[5:7])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[7:9]))))
        if channel in self.nicklists:
            self.nicklists[channel].append(nick)
        else:
            self.nicklists[channel]=[nick]
        if self.proxyscan:
            thread.start_new_thread(self.scan, (ip,channel,nick))
    def scan(self,ip,channel,nick):
        '''Preform a Nmap scan on the user to detect open ports that are commonly used to host open proxys used by spammers'''
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
            if ':?;' in self.ldata:
                self.findlist.append(data[data.find(':?; ')+4:].lower())
            elif ':?faster' in self.ldata:
                print(colorz.encode('FASTER','cayn'))
                self.wait=self.wait/2
            elif ':?slower' in self.ldata:
                print(colorz.encode('SLOWER','cayn'))
                self.wait=self.wait*2
            elif ':?setspeed ' in self.ldata:
                self.wait=float(data.split('?setspeed ')[-1][0:-2])
            elif ':?rehash' in self.ldata:
                self.__init__(self.__server__)
            elif ':?protect' in self.ldata:
                self.mode('',channel,'+mz')
        elif not self.superuser:
            self.checkforspam(nick,data,channel)
    def checkforspam(self,nick,data,channel):
        thread.start_new_thread(self.check_hilight,(nick,data,channel))
        self.msglist.insert(0,(nick,time.time(),data))
        if len(self.msglist)>5:
            self.msglist.pop()
        ident=data[data.find('@'):data.find(' PRIVMSG ')]
        ldata=data.lower()
        msg=ldata[ldata.find(' :')+2:]
        for each in self.findlist:
            if re.search(each,ldata):
                self.mode('*!*@%s'%api.getHost(data),channel,'+b')
                self.kick(nick,channel,'You have matched a spam string and have been banned from the channel, if you think this is a mistake, contact a channel op about being unbaned')
        try:
            if self.msglist[0][0]==self.msglist[1][0]==self.msglist[2][0]:
                if (self.msglist[0][1]-self.msglist[2][1])<self.wait:
                    self.kick(nick,channel,'It is against the rules to flood, you have been banned.')
                if msg.split()>1:
                    if (self.msglist[0][2]==self.msglist[1][2]==self.msglist[2][2]) and (self.msglist[0][1]-self.msglist[1][1]<self.repeat_time):
                        self.kick(nick,channel,'Please do not repeat!')
                        self.mode('*!*@%s'%api.getHost(data),channel,'+b')
        except IndexError:
            pass
    def get_notice(self,nick,channel,data):
        print colorz.encode('NOTICE Nick: %s; Channel: %s, Data: %s'%(nick,channel,data),'red')
        ldata=data.lower()
        self.olastnot=(self.lastnot[0:])
        self.lastnot=(nick,time.time())
        if self.olastnot[0]==self.lastnot[0]:
            if (self.lastnot[1]-self.olastnot[1])<self.wait:
                self.kick(nick,channel,'Please do not use the notice command so much')
        for each in self.findlist:
            if re.search(each,ldata):
                self.kick(nick,channel,'You have matched a spam string and have been banned. Please PM a channel opperator to be unbanned')
                self.mode(nick,channel,'+b')
    def check_hilight(self,nick,data,channel):
        '''Check to see if this person has pinged/hilighted over self.hilight_limit people, and if so, kick them'''
        print colorz.encode('Checking hilight spam','cayn')
        ldata=data[data.find(' :')+2:].lower()
        if not channel in self.nicklists:
            self.nicklists[channel]=[nick]
        found=0
        for each in self.nicklists[channel]:
            if each.lower() in ldata:
                found+=1
        if found>self.hilight_limit:
            self.kick(nick,channel,'Please do not ping that many people at one time.')
        print colorz.encode('Found: %s'%found,'cayn')
    def get_raw(self,type,data):
        print colorz.encode('Type: %s, Data: %s'%(type,data),'cayn')
        if type=='PART' or type=='KICK':
            try:
                if data[0] in self.nicklists[data[2]]:
                    self.nicklists[data[2]].pop(self.nicklists[data[2]].index(data[0]))
            except:
                pass
        elif type=='QUIT':
#            try:
            for channel in self.nicklists:
                print colorz.encode('Checking %s'%channel,'yellow')
                print colorz.encode(str(self.nicklists[channel]),'yellow')
                if data[0] in self.nicklists[channel]:
                    print colorz.encode('In %s'%channel,'green')
                    self.nicklists[channel].pop(self.nicklists[channel].index(data[0]))
#            except Exception,e:
#                print colorz.encode('%s,%s'%(type(e),e.args),'red')
        elif type=='CODE' and data[0]=='353':
            channel=data[1][data[1].find('= ')+2:data[1].find(' :')]
            names=data[1][data[1].find(' :')+2:].split()
            safe_names=[]
            for each in names:
                safe_names.append(each.strip('@+%'))#Add amp and tilda and parse 005
            for each in safe_names:
                self.nicklists[channel].append(each)
module=blockbot
