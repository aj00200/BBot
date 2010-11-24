import bbot,config,asynchat,asyncore,traceback,socket,time,api,re,colorz
class queue_class():
    def __init__(self):
        self.queue=[]
    def append(self,data):
        print colorz.encode('PRIVMSG '+data[0]+' :'+data[1],'green')
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

    def load_module(self,name):
        bbot.networks[self.server].append(__import__(name).module(self.server))
class connection(asynchat.async_chat,queue_class):
    def __init__(self,server):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_terminator('\r\n')
        self.data=''
        self.connect((server, config.port))
        self.server=server
        self.ac_in_buffer_size=config.wait_recv
        if not self.server in bbot.networks:
            bbot.networks[self.server]=[]
    def handle_connect(self):
        self.send('USER %s 8 %s :%s\r\n'%(config.mynick,config.network,'BBot the IRC bot')+'NICK %s\r\n'%config.mynick)
    def get_data(self):
        r=self.data
        self.data=''
        return r
    def found_terminator(self):
        data=self.get_data()
        if re.search(config.ignore,data):
            return #Ignore this
        print data
        if data[:4]==('PING'):
            self.push('PONG %s\r\n'%data[5:])
        if re.search(':*\.* 001 ',data):
            self.push('PRIVMSG nickserv :identify %s %s\r\n'%(config.username,config.password))
            time.sleep(2)
            for each in config.autojoin:
                self.push('JOIN %s\r\n'%each)
        if 'INVITE '+config.mynick+' :#' in data:
            if data.find(' 33')==-1 and data.find('NOTICE')==-1 and data.find('PRIVMSG')==-1 and data.find('KICK')==-1:
                newchannel=data.split(config.mynick+' :')[-1]
                self.push('JOIN '+newchannel+'\r\n')
        elif re.search(':(.)+!(.)+NOTICE #(.)+ :',data):
            nick=data[1:data.find('!')]
            channel=data[data.find(' NOTICE ')+8:data.find(' :')]
            words=data[data.find('NOTICE')+6:]
            words=words[words.find(':'):]
            for handler in bbot.networks[self.server]:
                handler.get_notice(nick,channel,words)
        elif ' PRIVMSG ' in data:
            channel=data[data.find(' PRIVMSG ')+9:data.find(' :')]
            nick=data[1:data.find('!')]
            for module in bbot.networks[self.server]:
                try:
                    module.go(nick,data,channel)
                except Exception,e:
                    if 'die' in e.args:
                        append(config.network,(config.error_chat,'Unrecoverable error raised by %s; It gave args: %s'%(module,type(e),e.args)))
                        raise die('An error occured in a module and the module requested that the bot be shutdown.')
                    append(config.network,(config.error_chan,'Error: %s; With args: %s; in %s'%(type(e),e.args,module)))
                    append(config.network,(config.error_chan,'Traceback: %s'%traceback.format_exc().replace('\n',' -- ')))
        elif ' JOIN :#' in data:
            nick=data.split('!')[0][1:]
            if nick.find('#')==-1:
                channel=data[data.find(' :#')+2:]
                ip=data[data.find('@')+1:data.find(' JOIN ')]
                user=data[data.find('!'):data.find('@')]
                for handler in bbot.networks[self.server]:
                    handler.get_join(nick,channel,ip,user)
        elif ' PART #' in data:
            nick=data[1:data.find('!')]
            w=data.split()
            for each in bbot.networks[self.server]:
                each.get_raw('PART',(nick,data,w[2]))
        elif ' KICK ' in data:
            w=data.split()
            for each in bbot.networks[self.server]:
                each.get_raw('KICK',(w[3],w[4],w[2]))
        elif ' QUIT ' in data:
            nick=data[1:data.find('!')]
            for each in bbot.networks[self.server]:
                each.get_raw('QUIT',(nick,data))
        elif re.search('[0-9]+ *'+config.mynick,data):
            code=data.split()[1]
            for each in bbot.networks[self.server]:
                each.get_raw('CODE',(code,data))
        elif data.find(' KILL ')!=-1:
            raise die('BBot has been killed')
    def collect_incoming_data(self,data):
        self.data+=data

connections={}
connections[config.network]=connection(config.network)
queue=connections[config.network]
def append(server,data):
    connections[server].append(data)
def kick(server,nick,channel,msg=''):
    connections[server].kick(nick,channel,msg)
def raw(server,data):
    connections[server].raw(data)

#===Errors===
class die(Exception):
    def __init__(self,error):
        self.args=[error]
