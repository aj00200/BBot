import q
import api
class searchbot(api.module):
    def __init__(self,server):
        self.goog='http://www.google.com/search?q=%s'
        self.wiki='http://www.en.wikipedia.org/wiki/%s'
        self.pb='http://www.pastebin.com/%s'
        self.upb='http://paste.ubuntu.com/%s'
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        if data.find(':?goog ')!=-1:
            w=data.split(':?goog ')[-1].replace(' ','+')
            self.append((channel,self.goog%w))
        elif data.find(':?wiki ')!=-1:
            w=data.split(':?wiki ')[-1].replace(' ','_')
            self.append((channel,self.wiki%w))
        elif data.find(':?pb ')!=-1:
            w=data.split(':?pb ')[-1]
            self.append((channel,self.pb%w))
        elif data.find(':?upb ')!=-1:
            w=data.split(':?upb ')[-1]
            self.append((channel,self.upb%w))
module=searchbot
