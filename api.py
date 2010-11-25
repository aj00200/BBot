backend=getattr(__import__('backends.async'),'async')
class module():
    def __init__(self,address):
        self.__address__=address
    def privmsg(self,nick,data,channel):
        '''Called every time a PRIVMSG is recieved'''
        print '* Go Message: (%s,%s,%s)'%(nick,data,channel)
    def append(self,channel,data=' '):
        print 'Use the NEW way to send things, msg(channel,data)'
    def msg(self,channel,data=' '):
        '''Send a message, data, to channel'''
        print 'PRIVMSG %s :%s'%(channel,data)
        backend.connections[self.__address__].push('PRIVMSG %s :%s\r\n'%(channel,data))
    def notice(self,channel,data):
        print ('NOTICE %s :%s'%(channel,data))
        backend.connections[self.__address__].push('NOTICE %s :%s'%(channel,data))
    def join(self,channel):
        backend.connections[self.__address__].push('JOIN %s'%channel)
    def part(self,channel):
        backend.connections[self.__address__].push('PART %s'%channel)
    def kick(self,channel,kickee,reason):
        backend.connections[self.__address__].push('KICK '+channel+' '+kickee+' :'+reason+'\r\n')
    def get_notice(self,nick,data,channel):
        '''Called every time a notice is recieved'''
        pass
    def get_join(self,nick,user,host,channel):
        pass
    def mode(channel,modes,nick=''):
        backend.connections[self.__address__].push('MODE '+channel+' '+modes+'\r\n')
    def raw(self,data):
        print '%s'%(data)
        backend.connections[self.__address__].push('%s\r\n'%(data))
