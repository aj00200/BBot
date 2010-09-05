import q
import re
import api
import time
import config
import thread
import colorz
import sqlite3
proxyscan=1
class blockbot(api.module):
    commands=['slower','faster','?;','setspeed','rehash','protect','sql']
    def sql(self):
        self.db=sqlite3.connect('database.sqlite')
        self.c=self.db.cursor()
        self.c.execute('create table if not exists lines (username text, line0 text, ts0 integer, line1 text, ts1 integer, line3 text, ts3 integer, line4 text, ts4 integer, line5 text, ts5 integer, line6 text, ts6 integer, line7 text, ts7 integer, line8 text, ts8)')
        try:
            self.c.execute('''create table recent (string, count, ts)''')
            self.c.commit()
        except:
            pass
        self.c=self.db.cursor()
        self.db.commit()
        self.db.close()
    def __init__(self,server):
        self.sql()
        self.ignore_users_on_su_list=1#Don't kick if they are on the superusers list
        self.nicklists={}
        self.hilight_limit=4
        self.config=open('blockbot-config','r')
        self.findlist=self.config.readline().lower()
        self.findlist=self.findlist[self.findlist.find(' ')+1:self.findlist.find('#')].split('^^^@@@^^^')
        if 'yes' in self.config.readline().lower():
            self.proxyscan=1
        else:
            self.proxyscan=0
        if self.proxyscan:
            import nmap #Can be found at: http://xael.org/norman/python/python-nmap/
        self.line=self.config.readline()
        self.wait=float(self.line[self.line.find(' ')+1:self.line.find('#')])
        self.config.close()
        self.repeatlimit=3
        self.repeat_time=3
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
                w=data[data.find(':?; ')+4:].lower()
                self.findlist.append(w)
                self.notice((channel,'<<%s has set a ban on %s>>'%(nick,w)))
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
                self.notice((channel,'<<BlockBot() has been rehashed>>'))
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
                self.kick(nick,channel,'You have matched a spam string and have been banned from the channel, if you think this is a mistake, contact a channel op about being unbanned')
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
        ldata=data.lower()
        self.olastnot=(self.lastnot[:])
        self.lastnot=(nick,time.time())
        if self.olastnot[0]==self.lastnot[0]:
            if (self.lastnot[1]-self.olastnot[1])<self.wait:
                self.kick(nick,channel,'Please don\'t use the notice command so much')
                self.mode(nick,channel,'+q')
        for each in self.findlist:
            if re.search(each,ldata):
                self.kick(nick,channel,'You have matched a spam string and have been banned. If this was a mistake, please contact a channel op to get unbanned')
                self.mode(nick,channel,'+b')
    def check_hilight(self,nick,data,channel):
        '''Check if nick has pinged more than self.hilight_limit people, and if so, kick them'''
        ldata=data[data.find(' :')+2:].lower()
        if channel not in self.nicklists:
            self.nicklists[channel]=[nick]
        found=0
        for each in self.nicklists[channel]:
            if each.lower() in ldata:
                found+=1
        if found>self.hilight_limit:
            self.kick(nick,channel,'Please do not ping that many people')
        #//////////////////////////////////////////////////////////////
        #///////////////////////////SQLite Code////////////////////////
        #//////////////////////////////////////////////////////////////
        try:
            self.db=sqlite3.connect('database.sqlite')
            self.c=self.db.cursor()
            msg=ldata[data.find(' :'):]
            current=['0',0,'0',0,'0',0,'0',0,'0',0,'0',0,'0',0]
            self.c.execute('''select * from lines''')
            for row in self.c:
                count=0
                print colorz.encode(str(row),'green')
                for each in range(0,len(row)):
                    if row[each]==msg:
                        count+=1
                if count>=self.repeatlimit-1: ##SQL Repeat Limit
                    self.kick(nick,channel,'Don\'t repeat yourself. We all heard the first time')
                    thread.start_new_thread(self.sql_add_str,(msg))
                if str(row[0])==nick:
                    current[0]=row[1]
                    current[1]=row[2]
                    current[2]=row[3]
                    current[3]=row[4]
                    current[4]=row[5]
                    current[5]=row[6]
                    current[6]=row[7]
                    current[7]=row[8]
                    current[8]=row[9]
                    current[9]=row[10]
                    current[10]=row[11]
                    current[11]=row[12]
                    current[12]=row[13]
            self.c.execute('''delete from lines where username=?''',(nick,))
            self.c.execute('''insert into lines values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(nick,msg,time.time(),current[0],current[1],current[2],current[3],current[4],current[5],current[6],current[7],current[8],current[9],current[10],current[11],current[11],current[12]))
        except Exception,e:
            print colorz.encode('Error: %s; %s'%(type(e),e.args),'red')
    #/////////////////////////END SQLite Code/////////////////////////
    def sql_add_str(self,msg):
        self.c.execute('''select * from recent where string=?''',(msg,))
        if len(self.c)>0:
            c=self.c[0][1]
            if c>2:
                self.findlist.append(msg[1:])
                self.c.execute('''delete from recent where string=?''',(msg,))
            else:
                c+=1
                self.c.execute('''delete from recent where string=?''',(msg,))
                self.c.execute('''insert into recent values(? ? ))''',(msg,c,time.time()))
    def get_raw(self,type,data):
        if type=='PART' or type=='KICK':
            try:
                if data[0] in self.nicklists[data[2]]:
                    self.nicklists[data[2]].pop(self.nicklists[data[2]].index(data[0]))
            except:
                pass
        elif type=='QUIT':
            try:
                for channel in self.nicklists:
                    if data[0] in self.nicklists[channel]:
                        self.nicklists[channel].pop(self.nicklists[channel].index(data[0]))
            except Exception,e:
                pass
        elif type=='CODE' and data[0]=='353':
            channel=data[1][data[1].find('= ')+2:data[1].find(' :')]
            names=data[1][data[1].find(' :')+2:].split()
            safe_names=[]
            for each in names:
                safe_names.append(each.strip('@+%'))#Add amp and tilda and parse 005
            if channel not in self.nicklists:
                self.nicklists[channel]=[]
            for each in safe_names:
                self.nicklists[channel].append(each)
module=blockbot
