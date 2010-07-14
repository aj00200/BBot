
import config
import asynchat
import asyncore
import socket
import api
class connection(asynchat.async_chat):
    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\r\n')
        self.data=''
        self.connect((config.network, config.port))
    def handle_connect(self):
        self.send('USER %s 8 %s :%s\r\n'%(config.mynick,config.network,'BBot the IRC bot')+'NICK B3Bot')
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
import bbot
