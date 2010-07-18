import q
import hashlib
import time
players={}
channel='#rpg'
op='FOSSnet/developer/aj00200'
class rpg():
    def __init__(self):
        self.objnames={
            0:'BasicSword',
            1:'BasicShield',
            2:'LightSwod',
            3:'LightShield'
        }
        self.objid={}
        for each in self.objnames:
            self.objid[self.objnames[each]]=each
        self.version='0.00011'
        self.turn=[]#list of nicks to get their turn
        self.TURN=[]
        self.lastturn=time.time()
        self.currentturn=0
    def go(self,nick,data,channel):
        try:
            if channel=='#rpg':
                self.ldata=data.lower()
                if self.ldata.find('?ver')!=-1:
                    q.queue.append((channel,self.version))
                if self.ldata.find('?join')!=-1:
                    if not nick in players:
                        players[nick]={
                            'health':100,
                            'spellpoints':100,
                            'objects':[0,1],
                            'id':hashlib.sha1(nick).hexdigest(),
                            'joined':time.time()
                            }
                        self.TURN.append(nick)
                        self.turn.append(nick)
                        q.queue.notice((channel,'<<%s has joined the game>>'%nick))
                if self.currentturn==nick:
                    if data.find('?attack ')!=-1:
                        self.vars=data[data.find('?attack ')+8:].split()
                        if self.vars[0] in players:
                            self.weapon=self.objid[self.vars[1].strip('\r\n')]
                            if self.weapon in self.objid:
                                q.queue.notice((channel,'%s attacks %s with a %s'%(nick,self.vars[0],self.vars[1])))
                if self.ldata.find('?rpg help')!=-1:
                    q.queue.append((nick,'Help comming soon. To join the game say ?join. To see your current status, type ?info.'))
                elif self.ldata.find('?info')!=-1:
                    if self.ldata.find('?info ')!=-1:
                        pass
                    else:
                        if nick in players:
                            self.msg='Info about %s: '%nick
                            self.msg+='%s: %s; '%('Health',players[nick]['health'])
                            self.msg+='%s: %s; '%('SpellPoints:',players[nick]['spellpoints'])
                            self.msg+='Objects: '
                            for each in players[nick]['objects']:
                                self.msg+='%s, '%self.objnames[each]
                                self.msg=self.msg[0:-2]#strip extra ', ' of the end
                                q.queue.notice((nick,self.msg))
                        else:
                            q.queue.notice((nick,'Please join the game with ?join'))
                elif self.ldata.find('?players')!=-1:
                    q.queue.append((channel,str(len(players))))
                elif self.ldata.find('?turn')!=-1:
                    q.queue.append((channel,'It is currently: %s\'s turn.'%self.currentturn))
        except Exception,e:
            q.queue.append((channel,'Error: %s; Args: %s'%(type(e),e.args)))
    def loop(self):
        if not self.currentturn and len(self.turn)>0:
            self.currentturn=self.turn.pop(0)
        if time.time()-self.lastturn>25:
            if len(self.turn):
                tmp=self.turn.pop(0)
                q.queue.notice((channel,'<<%s\'s turn has ended. It is now %s\'s turn>>'%(self.currentturn,tmp)))
                self.currentturn=tmp[:]
                self.lastturn=time.time()
            else:
                self.turn=self.TURN[:]
