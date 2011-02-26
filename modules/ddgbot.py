import api, config
import urllib, thread, re
import json
from xml.dom.minidom import parse, parseString

class Module(api.module):
    '''A module for preforming web lookups of various
    facts. Responds to "what is" questings best'''
    url = 'https://duckduckgo.com/?q=%s&o=xml'
    freebase = 'https://api.freebase.com/api/experimental/topic/standard?id=/en/%s'
    def __init__(self, address):
        api.module.__init__(self, address)
        api.hook_command('define', self.ddg_define, address)

    def privmsg(self, nick, data, channel):
         if ':'+config.cmd_char+'ddg ' in data:
                query = data[data.find('ddg ')+4:]
                thread.start_new_thread(self.ddg, (nick, data, channel, query))
         ldata = data.lower()
         ldata = ldata.replace('whats', 'what is').replace("what's", 'what is')
         if re.search('(what|who|where) (is|was|are|am) ', ldata):
                ldata = ldata.replace(' was ', ' is ')
                ldata = ldata.replace(' a ', ' ')
                ldata = ldata.replace(' the ', ' ')
                ldata = ldata.replace(' was ', ' ')
                ldata = ldata.replace(' an ', ' ')
                ldata = ldata.replace(' are ', ' is ')
                qu = 'what is '+ldata[ldata.find(' is ')+4:]
                self.ddg(nick, data, channel, qu, reply_on_notfound = False)
                #self.fb(nick, data, channel, qu, reply_on_notfound = True)

    def ddg_define(self, nick, channel, param = None):
        self.ddg(nick, channel, 'define %s' % param, reply_on_notfound = True)

    def ddg(self, nick, channel, query, reply_on_notfound = True):
         t = urllib.urlretrieve(self.url%urllib.quote_plus(query))
         xml = parse(t[0])
         try:
                t = str(xml.getElementsByTagName('AbstractText')[0].childNodes[0].wholeText)
                self.msg(channel, '%s: %s'%(nick, t))
         except:
                try:
                    t = str(xml.getElementsByTagName('Answer')[0].childNodes[0].wholeText)
                    self.msg(channel, '%s: %s'%(nick, t))
                except:
                    if reply_on_notfound:
                         self.msg(channel, '%s: Sorry, but I could not find what %s is'%(nick, query))

    def fb(self, nick, channel, query, reply_on_notfound = True):
        '''Query Freebase for the query'''
        qu = query.replace(' ', '_').replace('what_is_', '')
        t = urllib.urlopen(self.freebase%urllib.quote_plus(qu))
        j = json.load(t)
        try:
            r = j['/en/%s' % qu]['result']['description']
            self.msg(channel, '%s: %s' % (nick, r.split('. ')[0]))
        except Exception, e:
            print j['/en/%s'%qu]
            print 'Error: %s, %s' % (e.__repr__(), e.args)
            if reply_on_notfound:
                self.msg(channel, '%s: Sorry, could not find it'%nick)
