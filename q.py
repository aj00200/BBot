import bbot
#if __name__!='__main__':
#    reload(bbot)
import config
import asynchat
import asyncore
import socket
import api
import re
class queue_class():
    def __init__(self):
        self.queue=[]
    def append(self,data):
        self.go('PRIVMSG '+data[0]+' :'+data[1])
    def join(self, channel):
        self.go('JOIN '+channel)
    def part(self, channel, message=''):
        self.go('PART %s :%s'%(channel,message))
    def kick(self,nick,channel,message=''):
        self.go('KICK %s %s :%s!'%(channel,nick,message))
    def nick(self,nick):
        self.go('NICK %s'%nick)
        mynick=nick[:]
    def notice(self,data):
        self.go('NOTICE '+data[0]+' :'+data[1])
    def mode(self,nick,channel,mode):
        self.go('MODE '+channel+' '+mode+' '+nick)
    def kill(self,nick,reason=''):#Must be IRCOP
        self.go('KILL %s :%s' % (nick,reason))
    def kline(self,host,time='3600',reason='K-Lined'):#Must be IRCOP
        self.go('KLINE %s %s :%s'%(host,str(time),reason))
    def raw(self,data):
        self.go(data)
    def go(self,data):
        self.push(data+'\r\n')
class connection(asynchat.async_chat,queue_class):
    def __init__(self,server):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\r\n')
        self.data=''
        self.connect((server, config.port))
    def handle_connect(self):
        self.send('USER %s 8 %s :%s\r\n'%(config.mynick,config.network,'BBot the IRC bot')+'NICK %s\r\n'%config.mynick)
    def get_data(self):
        r=self.data
        self.data=''
        return r
    def found_terminator(self):
        data=self.get_data()
        print data
        if data[:4]==('PING'):
            self.push('PONG %s\r\n'%data[5:])
        if re.search(':*\.* 001 ',data):
            for each in config.autojoin:
                self.push('JOIN %s\r\n'%each)
        if data.find('INVITE '+config.mynick+' :#')!=-1:
            if data.find(' 33')==-1 and data.find('NOTICE')==-1 and data.find('PRIVMSG')==-1 and data.find('KICK')==-1:
                newchannel=data.split(config.mynick+' :')[-1]
                self.push('JOIN '+newchannel+'\r\n')
                del newchannel
        elif re.search(':*!*NOTICE #*:',data):
            nick=data[1:data.find('!')]
            channel=data[data.find(' NOTICE ')+8:data.find(':')]
            words=data[data.find('NOTICE')+6:]
            words=words[words.find(':'):]
            for handler in bbot.nhandlers:
                handler.notice(nick,channel,words)
        elif data.find(' PRIVMSG ')!=-1:
            channel=data.split(' PRIVMSG ')[1]
            channel=channel.split(' :')[0]
            nick=data.split('!')[0][1:]
            for handler in bbot.handlers:
                handler.go(nick,data,channel)
        elif data.find(' JOIN :#')!=-1:
            nick=data.split('!')[0][1:]
            if nick.find('#')==-1:
                channel='#'+data.split(' :#')[-1][0:-2]
                ip=data.split('@')[1].split(' JOIN')[0]
                user=data.split('@')[0].split('!')[-1]
                for jhandler in bbot.jhandlers:
                    jhandler.join(nick,channel,ip,user)
        elif re.search('[0-9]+ *'+config.mynick,data):
            code=data.split()[1]
            for each in bbot.codes:
                each.code(code,data)
        if data.strip('\r\n')=='':
            continuepgm=0
        for handler in bbot.lhandlers:
            handler.loop()
    def collect_incoming_data(self,data):
        self.data+=data
connections={}
connections[config.network]=connection(config.network)
queue=connections[config.network]
def append(server,data):
    connections[server].append((data))
