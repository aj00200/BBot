import q
import bbot
import colorz
def getHost(data):
    host=data[data.find('@')+1:data.find('PRIVMSG')]
    return host
def checkIfSuperUser(data,superusers):
    host=getHost(data)
    for su in superusers:
        if host.find(su)!=-1:
            return True
    else:
        return False
def pong(data):
    if data.find ('PING')!=-1:
        print('PING RECEIVED')
        q.queue.raw('PONG '+data.split()[ 1 ]+'\r\n') #Return the PING to the server
        print('PONGING')
def add_networkk(server):
    bbot.add_network(server)
class module():
    def __init__(self,server):
        self.__server__=server
    def append(self,data):
        q.append(self.__server__,data)
    def join(self, channel):
        q.raw(self.__server__,'JOIN '+channel)
    def part(self, channel, message=''):
        q.raw(self.__server__,'PART %s :%s'%(channel,message))
    def kick(self,nick,channel,message=''):
        q.kick(self.__server__,nick,channel,message)
    def nick(self,nick):
        q.append(self.__server__,'NICK %s'%nick)
        bbot.mynick=nick[:]
    def notice(self,data):
        q.raw(self.__server__,'NOTICE '+data[0]+' :'+data[1])
    def mode(self,nick,channel,mode):
        q.raw(self.__server__,'MODE '+channel+' '+mode+' '+nick)
    def kill(self,nick,reason=''):#Must be IRCOP
        q.append(self.__server__,'KILL %s :%s' % (nick,reason))
    def kline(self,host,time='3600',reason='K-Lined'):#Must be IRCOP
        q.raw(self.__server__,'KLINE %s %s :%s'%(host,str(time),reason))
    def raw(self,data):
        q.raw(self.__server__,data)
    def go(self,nick,data,channel):
        pass
    def notice(self,nick,data,channel):
        pass
