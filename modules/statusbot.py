import q,api,time,thread
class module(api.module):
    commands=['status','whereis','notify','timer','rawtimer']
    def __init__(self,server):
        self.statuses={}
        api.module.__init__(self,server)
    def privmsg(self,nick,data,channel):
        if ':?status ' in data:
            words=data[data.find('status ')+7:]
            self.statuses[nick.lower()]=words
        elif 'whereis' in data:
            who=data[data.find('whereis ')+8:]
            if who in self.statuses:
                self.msg(channel,'%s: %s\'s status is: %s'%(nick,who,self.statuses[who]))
        if api.checkIfSuperUser(data):
            if '?timer' in data:
                words=data[data.find('timer ')+8:]
                words=words.split('m ',1)
                thread.start_new_thread(self.timer,(words[0],'PRIVMSG %s :%s'%(channel,words[1])))
            elif '?rawtimer ' in data:
                words=data[data.find(':?rawtimer ')+10:]
                words=words.split('m ',1)
                thread.start_new_thread(self.timer,(words[0],words[1]))
    def timer(self,wait,message):
        time.sleep(float(wait)*60)
        self.raw(message)
