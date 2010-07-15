import bbot
import config
import asynchat
import asyncore
import socket
import api
import re

class connection(asynchat.async_chat):
    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\r\n')
        self.data=''
        self.connect((config.network, config.port))
    def handle_connect(self):
        self.send('USER %s 8 %s :%s\r\n'%(config.mynick,config.network,'BBot the IRC bot')+'NICK B3Bot\r\n')
    def get_data(self):
        r=self.data
        self.data=''
        return r
    def found_terminator(self):
        data=self.get_data()
        print data
        if data[:4]==('PING'):
            self.push('PONG %s\r\n'%data[5:])
        if '001' in data:
            self.push('JOIN %s\r\n'%', '.join(config.autojoin))
        if data.find('INVITE '+config.mynick+' :#')!=-1:
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
            if data.find('?reload')!=-1:
                del rb
                handlers.pop()
                lhandlers.pop()
                reload(rpgbot)
                rb=rpgbot.rpg()
                handlers.append(rb)
                lhandlers.append(rb)
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
        queue.send()
    def collect_incoming_data(self,data):
        self.data+=data
class queue_class():
    def __init__(self):
        self.queue=[]
        self.conn=connection()
    def send(self):
        for each in self.queue:
            print('PUSHING')
            self.conn.push(each+'\r\n')
        self.queue=[]
    def get_length(self):
        return len(self.queue)
    def append(self,data):
        self.queue.append('PRIVMSG '+data[0]+' :'+data[1])
    def pop(self):
        return self.queue.pop(0)
    def join(self, channel):
        self.queue.append('JOIN '+channel)
    def part(self, channel, message=''):
        self.queue.append('PART %s :%s'%(channel,message))
    def kick(self,nick,channel,message=''):
        self.queue.append('KICK %s %s :%s!'%(channel,nick,message))
    def nick(self,nick):
        self.queue.append('NICK %s'%nick)
        mynick=nick[:]
    def notice(self,data):
        self.queue.append('NOTICE '+data[0]+' :'+data[1])
    def mode(self,nick,channel,mode):
        self.queue.append('MODE '+channel+' '+mode+' '+nick)
    def kill(self,nick,reason=''):#Must be IRCOP
        self.queue.append('KILL %s :%s' % (nick,reason))
    def kline(self,host,time='3600',reason='K-Lined'):#Must be IRCOP
        self.queue.append('KLINE %s %s :%s'%(host,str(time),reason))
    def raw(self,data):
        self.queue.append(data)
queue=queue_class() 

