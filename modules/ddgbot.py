import api,config
import urllib,thread,re
from xml.dom.minidom import parse, parseString
class module(api.module):
    commands=['ddg']
    url='https://duckduckgo.com/?q=%s&o=x'
    def privmsg(self,nick,data,channel):
        if ':'+config.cmd_char+'ddg ' in data:
            query=data[data.find('ddg ')+4:]
            thread.start_new_thread(self.ddg,(nick,data,channel,query))
        ldata=data.lower()
        ldata=ldata.replace('whats','what is').replace("what's",'what is')
        if re.search('(what|who|where) (is|was|are|am) ',ldata):
            ldata=ldata.replace(' was ',' is ')
            ldata=ldata.replace(' a ',' ')
            ldata=ldata.replace(' the ',' ')
            ldata=ldata.replace(' was ',' ')
            ldata=ldata.replace(' an ',' ')
            ldata=ldata.replace(' are ',' is ')
            self.ddg(nick,data,channel,'what is '+ldata[ldata.find(' is ')+4:],reply_on_notfound=False)
    def ddg(self,nick,data,channel,query,reply_on_notfound=True):
        t=urllib.urlretrieve(self.url%urllib.quote_plus(query))
        xml=parse(t[0])
        try:
            t=str(xml.getElementsByTagName('AbstractText')[0].childNodes[0].wholeText)
            self.msg(channel,'%s: %s'%(nick,t))
        except:
            try:
                t=str(xml.getElementsByTagName('Answer')[0].childNodes[0].wholeText)
                self.msg(channel,'%s: %s'%(nick,t))
            except:
                if reply_on_notfound:
                    self.msg(channel,'%s: Sorry, but I couldn\'t find what %s is'%(nick,query))
