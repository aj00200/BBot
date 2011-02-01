"""This module implements flood control and anti-spam measures."""

import re,api,time,config,thread,colorz,sqlite3
class module(api.module):
    def __init__(self,server):
        api.module.__init__(self,server)
        api.register_commands(self.__address__,['?;','rehash'])
        self.nicklists={}
        self.hilight_limit=api.getConfigInt('BlockBot','hilight-limit')
        findlist=api.getConfigStr('BlockBot','spam-strings').split('^^^@@@^^^')
        self.findlist=[]
        for each in findlist:
            self.findlist.append(re.compile(each))
        self.flood_speed=api.getConfigFloat('BlockBot','flood-speed')
        self.repeatlimit=3
        self.repeat_time=3
        self.repeat_1word=4
        self.msglist=[]
        self.lastnot=('BBot',time.time(),'sdkljfls')

    def privmsg(self,nick,data,channel):
        self.ldata=data.lower()
        if api.checkIfSuperUser(data,config.superusers):
            if ' :?; ' in self.ldata:
                word=data[data.find(' :'+config.cmd_char+'; ')+4+len(config.cmd_char):]
                self.findlist.append(word)
        else:
	        thread.start_new_thread(self.check_hilight,(nick,data,channel))
	        self.msglist.insert(0,(nick,time.time(),data))
	        if len(self.msglist)>5:
	            self.msglist.pop()
	        ident=data[data.find('@'):data.find(' PRIVMSG ')]
	        ldata=data.lower()
	        msg=ldata[ldata.find(' :')+2:]
	        for each in self.findlist:
	            if re.search(each,ldata):
	                self.kick(nick,channel,'You have matched a spam string and have been banned from the channel, if you think this is a mistake, contact a channel op about being unbanned')
	                return 0
	        try:
	            if self.msglist[0][0]==self.msglist[1][0]==self.msglist[2][0]:
	                if (self.msglist[0][1]-self.msglist[2][1])<self.flood_speed:
	                    self.kick(nick,channel,'It is against the rules to flood')
	                    return 0
	                elif msg.split()>1:
	                    if (self.msglist[0][2]==self.msglist[1][2]==self.msglist[2][2]) and (self.msglist[0][1]-self.msglist[1][1]<self.repeat_time):
	                        self.kick(nick,channel,'Please do not repeat')
	                        self.mode('*!*@%s'%api.getHost(data),channel,'+b')
	        except IndexError:
	            pass
    def check_hilight(self,nick,data,channel):
        '''Check if nick has pinged more than self.hilight_limit people, and if so, kick them'''
        ldata=data[data.find(' :')+2:].lower()
        if channel not in self.nicklists:
            self.nicklists[channel]=[nick.lower()]
        found=0
        for each in self.nicklists[channel]:
            if each in ldata:
                found+=1
        if found>self.hilight_limit:
            print '* kicking %s out of %s'%(nick,channel)
            self.kick(nick,channel,'Please do not ping that many people')

    def get_join(self,nick,channel,ip,user):
        '''Add user to nicklist, and preform optional proxy scan'''
        if channel in self.nicklists and nick not in self.nicklists[channel]:
            self.nicklists[channel].append(nick)
        else:
            self.nicklists[channel]=[nick]
    def get_notice(self,nick,channel,data):
        ldata=data.lower()
        self.olastnot=(self.lastnot[:])
        self.lastnot=(nick,time.time())
        if self.olastnot[0]==self.lastnot[0]:
            if (self.lastnot[1]-self.olastnot[1])<self.flood_speed:
                self.kick(nick,channel,'Please don\'t use the notice command so much')
                self.mode(channel,'+q',nick)
        for each in self.findlist:
            if re.search(each,ldata):
                self.kick(nick,channel,'You have matched a spam string and have been banned. If this was a mistake, please contact a channel op to get unbanned')
                self.mode(nick,channel,'+b')
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
                safe_names.append(each.strip('@+%~').lower())#Add amp and tilda and parse 005
            if channel not in self.nicklists:
                self.nicklists[channel]=[]
            for each in safe_names:
                self.nicklists[channel].append(each)
