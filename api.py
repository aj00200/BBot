class module():
    def __init__(self,address):
        self.__address__=address
    def privmsg(self,nick,data,channel):
        print '* Go Message: (%s,%s,%s)'%(nick,data,channel)
    def append(self,channel,data=' '):
        print '*PRIVMSG %s %s'%(channel,data)
