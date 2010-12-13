import config
backend=getattr(__import__('backends.async'),'async')
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
class module():
    '''Base class that all modules should use to maintain best compatibility with future versions of the API'''
    commands=[]
    def __init__(self,address):
        self.__address__=address
    def privmsg(self,nick,data,channel):
        '''Called every time a PRIVMSG is recieved'''
        pass
    def append(self,channel,data=' '):
        print 'Use the NEW way to send things, msg(channel,data)'
    def msg(self,channel,data=' '):
        '''Send a message, data, to channel'''
        print 'PRIVMSG %s :%s'%(channel,data)
        backend.connections[self.__address__].push('PRIVMSG %s :%s\r\n'%(channel,data))
    def notice(self,channel,data):
        print ('NOTICE %s :%s'%(channel,data))
        backend.connections[self.__address__].push('NOTICE %s :%s\r\n'%(channel,data))
    def join(self,channel):
        backend.connections[self.__address__].push('JOIN %s\r\n'%channel)
    def part(self,channel):
        backend.connections[self.__address__].push('PART %s\r\n'%channel)
    #def kick(self,channel,kickee,reason):
      #  backend.connections[self.__address__].push('KICK %s %s :%s\r\n'%(channel,kickee,reason))
    def kick(self,nick,channel,message=''): #nick,channel,message)
        backend.connections[self.__address__].push("KICK "+channel+" "+nick+" :"+message+"\r\n")
    def get_notice(self,nick,data,channel):
        '''Called every time a notice is recieved'''
        pass
    def get_join(self,nick,user,host,channel):
        pass
    def get_raw(self,type,params):
        '''Called every time a message that does not fall into the other categories is recieved:
            type is set to 'CODE' when messages that corespond to a numberic code are recieved'''
        pass
    def mode(self,nick,channel,mode):
        backend.connections[self.__address__].push('MODE '+channel+' '+mode+' '+nick+'\r\n')
    def raw(self,data):
        print '%s'%(data)
        backend.connections[self.__address__].push('%s\r\n'%(data))
