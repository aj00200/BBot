import q
import bbot
import config
import colorz
def getConfigStr(cat,name):
    return config.c.get(cat,name)
def getConfigInt(cat,name):
    return config.c.getint(cat,name)
def getConfigFloat(cat,name):
    return config.c.getfloat(cat,name)
def getConfigBool(cat,name):
    return config.c.getboolean(cat,name)
def getHost(data):
    '''Returns the hostname (IP address) of the person who sent the message passed to the variable data'''
    return data[data.find('@')+1:data.find(' ')]
def getNick(data):
    '''Returns the nickname of the person who sent the message passed to this function'''
    return data[1:data.find('!')]
def getIdent(data):
    '''Returns the ident of the person who sent the message passed to this function'''
    return data[data.find('!')+1:data.find('@')]
def getMessage(data):
    '''Returns the actual message that was sent without the nickname, hostname, and so on'''
    return data[data.find(' :')+2:]
def hostInList(data,list):
    '''Tells you if the host of the person who sent the message that is pased as the first arg is in the list of hosts which is the second arg'''
    host=getHost(data)
    for su in list:
        if host.find(su)!=-1:
            return True
    else:
        return False
def checkIfSuperUser(data,superusers=config.superusers):
    return hostInList(data,superusers)
def pong(data):
    if data.find ('PING')!=-1:
        q.queue.raw('PONG '+data.split()[ 1 ]+'\r\n') #Return the PING to the server
def add_networkk(server):
    bbot.add_network(server)
class module():
    commands=[]
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
        q.raw(self.__server__,'NICK %s'%nick)
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
        '''Called every time a message is received'''
        pass
    def get_notice(self,nick,channel,data):
        pass
    def get_raw(self,type,data):
        pass
    def get_join(self,nick,channel,ip,user):
        '''Called eveery time someone joins a channel'''
        pass
    def loop(self):
        '''Called every 5 seconds'''
        pass
    def destroy(self):
        '''Called when the module is unloaded'''
        pass
