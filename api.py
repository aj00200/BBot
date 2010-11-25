backend=getattr(__import__('backends.async'),'async')
class module():
    def __init__(self,address):
        self.__address__=address
    def privmsg(self,nick,data,channel):
        print '* Go Message: (%s,%s,%s)'%(nick,data,channel)
    def append(self,channel,data=' '):
        print 'Use the NEW way to send things, msg(channel,data)'
    def msg(self,channel,data=' '):
        print 'PRIVMSG %s :%s'%(channel,data)
        backend.connections[self.__address__].push('PRIVMSG %s :%s\r\n'%(channel,data))
