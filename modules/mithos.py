import re,api,time,config,thread,colorz,sqlite3
proxyscan=1
class module(api.module):
    def kickBan(self,channel,nick,host,reason):
                self.mode('*!*@%s'%host,channel,'+b')
                self.kick(nick,channel,reason)
    def __init__(self,server):
        self.repeat10 = "0"
        self.repeat9 = "0"
        self.repeat8 = "0"
        self.repeat7 = "0"
        self.repeat6 = "0"
        self.repeat5 = "0"
        self.repeat4 = "0"
        self.repeat3 = "0"
        self.repeat2 = "0"
        self.repeat1 = "0"
        self.repeat0 = "0"
        self.ignore_users_on_su_list=1#Don't kick if they are on the superusers list
        self.nicklists={}
        self.hilight_limit=api.getConfigInt('BlockBot','hilight-limit')
        self.config=open('mithos-config','r')
        findlist=self.config.readline().lower()
        findlist=findlist[findlist.find(' ')+1:findlist.find('#')].split('^^^@@@^^^')
        self.findlist=[]
        for each in findlist:
            self.findlist.append(re.compile(each))
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
        '''Add user to nicklist, and preform optional proxy scan [proxy scan disabled in mithos.py]'''
        #webchat=(str(blockbotlib.hex2dec('0x'+str(user[1:3])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[3:5])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[5:7])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[7:9]))))
        if channel in self.nicklists:
            self.nicklists[channel].append(nick)
        else:
            self.nicklists[channel]=[nick]
    def privmsg(self,nick,data,channel):
        self.ldata=data.lower()
        if self.ignore_users_on_su_list:
            self.superuser=api.checkIfSuperUser(data,config.superusers)
        if self.superuser:
            if ':?;' in self.ldata:new_thread(self.check_hilight,(nick,data,channel))
        self.msglist.insert(0,(nick,time.time(),data))
        if len(self.msglist)>5:
            self.msglist.pop()
        ident=data[data.find('@'):data.find(' PRIVMSG ')]
        ldata=data.lower()
        msg=ldata[ldata.find(' :')+2:]
        debug = 1
        if debug == 1:
            self.repeat10 = self.repeat9
            self.repeat9 = self.repeat8
            self.repeat8 = self.repeat7
            self.repeat7 = self.repeat6
            self.repeat6 = self.repeat5
            self.repeat5 = self.repeat4
            self.repeat4 = self.repeat3
            self.repeat3 = self.repeat2
            self.repeat2 = self.repeat1
            self.repeat1 = self.repeat0
            self.repeat0 = msg
            if msg.split()>3:
				if self.repeat0 == self.repeat1 and self.repeat0 == self.repeat2 or self.repeat0 == self.repeat3 or self.repeat0 == self.repeat4 or self.repeat0 == self.repeat5 or self.repeat0 == self.repeat6 or self.repeat0 == self.repeat7 or self.repeat0 == self.repeat8 or self.repeat0 == self.repeat9 or self.repeat0 == self.repeat10:
					self.raw("PRIVMSG #bikcmp :repeating!")
        for each in self.findlist:
			
            if re.search(each,ldata):
				#self,channel,nick,api.getHost(data),reason
                self.kickBan(channel,nick,api.getHost(data),"Matched spam string")
                return 0
        try:
            if self.msglist[0][0]==self.msglist[1][0]==self.msglist[2][0]:
                if (self.msglist[0][1]-self.msglist[2][1])<self.wait:
                    self.kick(nick,channel,'It is against the rules to flood')
                    return 0
                elif msg.split()>1:
                    if (self.msglist[0][2]==self.msglist[1][2]==self.msglist[2][2]) and (self.msglist[0][1]-self.msglist[1][1]<self.repeat_time):
                        self.kickBan(channel,nick,api.getHost(data),"Please do not repeat!")
        except IndexError:
            pass
         
    def get_notice(self,nick,channel,data):
        ldata=data.lower()
        self.olastnot=(self.lastnot[:])
        self.lastnot=(nick,time.time())
        if self.olastnot[0]==self.lastnot[0]:
            if (self.lastnot[1]-self.olastnot[1])<self.wait:
                self.kickBan(channel,nick,api.getHost(data),"Please don't use the notice command so much")
        for each in self.findlist:
            if re.search(each,ldata):
                self.kickBan(channel,nick,api.getHost(data),'You have matched a spam string and have been banned. If this was a mistake, please contact a channel op to get unbanned')
      
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
            self.kickBan(channel,nick,api.getHost(data),"Please do not ping that many people!")
        #//////////////////////////////////////////////////////////////
        #///////////////////////////Repeat Code////////////////////////
        #//////////////////////////////////////////////////////////////
        #try:
        
        #~ except Exception,e:
            #~ print colorz.encode('Error: %s; %s'%(type(e),e.args),'red')
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
