import q
class statusbot():
    def __init__(self):
        self.statuses={}
    def go(self,nick,data,channel):
        if data.find(':?status ')!=-1:
            words=data.split('?status')[-1].strip('\r\n')
            self.statuses[nick]=words[:]
        elif data.find(':?whereis ')!=-1:
            try:
                words=data.split(':?whereis ')[-1].strip('\r\n')
                q.queue.append((channel,nick+': %s is: '%words+self.statuses[words]))
            except:
                q.queue.append((channel,nick+': %s hasn\'t left a status.'%words))
        elif data.find('?notify ')!=-1:
            words=data.split(':?notify ')[-1].strip('\r\n').strip('#')
            if words.find(' '):
                q.queue.append((nick,'Please don\'t abuse me. This is logged!'))
            else:
                queue.append((words,'Just letting you know, %s is looking for you in %s' % (nick,channel)))
        elif data.find(':?reset')!=-1:
            words=data.split(':?reset')[-1].strip('\r\n')
            try:
                del self.statuses[words]
            except:
                pass