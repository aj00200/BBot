import q,api,time,thread
class statusbot(api.module):
    commands=['status','whereis','notify','timer','rawtimer']
    def __init__(self,server):
        self.statuses={}
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        self.ldata=data.lower()
        if data.find(':?status ')!=-1:
            words=data.split('?status ')[-1].strip('\r\n')
            self.statuses[nick.lower()]=words[:]
        elif self.ldata.find(':?whereis ')!=-1:
            try:
                words=self.ldata.split(':?whereis ')[-1].strip('\r\n')
                self.append((channel,nick+': %s is: '%words+self.statuses[words]))
            except:
                self.append((channel,nick+': %s hasn\'t left a status.'%words))
        elif data.find(':?notify ')!=-1:
            words=data.split(':?notify ')[-1].strip('\r\n').strip('#')
            if words.find(' ')!=-1:
                self.append((nick,'Please don\'t abuse the bot. This is loged!'))
            else:
                self.append((words,'Just letting you know, %s is looking for you in %s' % (nick,channel)))
        if api.checkIfSuperUser(data):
            if data.find(':?reset')!=-1:
                words=data.split(':?reset ')[-1].strip('\r\n')
                try:
                    del self.statuses[words]
                except:
                    pass
            elif data.find(':?timer ')!=-1:
                words=data[data.find('timer ')+8:]
                words=words.split('m ',1)
                thread.start_new_thread(self.timer,(words[0],'PRIVMSG %s :%s'%(channel,words[1])))
            elif data.find('?rawtimer ')!=-1:
                words=data[data.find(':?rawtimer ')+10:]
                words=words.split('m ',1)
                thread.start_new_thread(self.timer,(words[0],words[1]))
    def timer(self,wait,message):
        time.sleep(float(wait)*60)
        self.raw(message)
module=statusbot
