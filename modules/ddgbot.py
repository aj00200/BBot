import q,api,config
import urllib,thread,re
from xml.dom.minidom import parse, parseString
class module(api.module):
    commands=['ddg']
    url='https://duckduckgo.com/?q=%s&o=x'
    def go(self,nick,data,channel):
        if ':'+config.cmd_char+'ddg ' in data:
            query=data[data.find('ddg ')+4:]
            thread.start_new_thread(self.ddg,(nick,data,channel,query))
        ldata=data.lower()
        ldata=ldata.replace('whats','what is').replace('what\'s','what is')
        if re.search('(what|who|where) (is|was|are|am) ',ldata):
            self.ldata=ldata.replace(' was ',' is ')
            self.ldata=self.ldata.replace(' a ',' ')
            self.ldata=self.ldata.replace(' the ',' ')
            self.ldata=self.ldata.replace(' was ',' ')
            self.ldata=self.ldata.replace(' an ',' ')
            self.ldata=self.ldata.replace(' are ',' is ')
            self.ddg(nick,data,channel,'what is '+data[data.find(' is ')+4:],reply_on_notfound=False)
    def ddg(self,nick,data,channel,query,reply_on_notfound=True):
        t=urllib.urlretrieve(self.url%urllib.quote_plus(query))
        xml=parse(t[0])
        try:
            t=str(xml.getElementsByTagName('AbstractText')[0].childNodes[0].wholeText)
            self.append((channel,'%s: %s'%(nick,t)))
        except:
            try:
                t=str(xml.getElementsByTagName('Answer')[0].childNodes[0].wholeText)
                self.append((channel,'%s: %s'%(nick,t)))
            except:
                if reply_on_notfound:
                    self.append((channel,'%s: Sorry, but I couldn\'t find what %s is'%(nick,query)))
