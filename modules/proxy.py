import q
import thread
class proxy():
    def __init__(self):
        self.continue=1
        self.irc=socket.socket()
        self.irc.connect(('irc.freenode.net','6667'))
#        thread.
    def loop(self):
        self.needping=1
        while self.needping:
            self.data=irc.recv(1024)
            if data.find('PING')!=-1:
                self.pong(self.data)
                needping=0
        self.irc.send('JOIN #bbot')
        while self.continue:
            self.data=irc.recv(4096)
            self.pong(self.data)
            if data.find(' PRIVMSG #bbot :')!=-1:
                self.nick=self.data[1:self.data.find('!')]
                self.msg=self.data[data.find(' :'):]
                q.queue.append(('#bbot','<%s> %s'%(self.nick,self.msg)))
    def pong(data):
        if data.find('PING')!=-1:
            irc.send(data.split()[1]+'\r\n')
    def go(self,nick,data,channel):
        if channel=='#bbot':
            self.msg2=data[data.find(' :'):]
            self.irc.send('PRIVMSG #bbot :<%s> %s'%(nick,self.msg2+'\r\n')
module=proxy
