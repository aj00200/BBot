'''Query the Duck Duck Go one-click info API for information requested
inside of an IRC channel.
'''
import urllib, re
import json
import api

class Module(api.Module):
    '''A module for preforming web lookups of various
    facts. Responds to "what is" questings best'''
    urls = {
        'ddg': 'https://duckduckgo.com/?q=%s&o=json&d=1',
        'fb': 'https://api.freebase.com/api/experimental/topic/standard?id=/en/%s'
    }
    def __init__(self, server):
        super(Module, self).__init__(server)
        api.hook_command('ddg', self.ddg, server)
        api.hook_command('define', self.ddg_define, server)

    def privmsg(self, nick, data, channel):
        ldata = data.lower()
        ldata = ldata.replace('whats', 'what is').replace("what's", 'what is')
        if re.search('(what|who|where) (is|was|are|am) ', ldata):
            ldata = ldata.replace(' was ', ' is ')
            ldata = ldata.replace(' a ', ' ')
            ldata = ldata.replace(' the ', ' ')
            ldata = ldata.replace(' was ', ' ')
            ldata = ldata.replace(' an ', ' ')
            ldata = ldata.replace(' are ', ' is ')
            query = ldata[ldata.find(' is ')+4:]
            self.ddg(nick, channel, query, reply_on_notfound = False)
            #self.freebase(nick, data, channel, qu, reply_on_notfound = True)

    def ddg_define(self, nick, channel, param = None):
        '''Look up a definition of a word.'''
        self.ddg(nick, channel, 'define %s' % param, reply_on_notfound = True)

    def ddg(self, nick, channel, param = None, reply_on_notfound = True):
        '''Preform a DDG lookup of a query; Parameters: query'''
        if not param:
            self.msg(channel, '%s: you must include a query.' % nick)
        else:
            url = self.urls['ddg'] % urllib.quote_plus(param)
            data = urllib.urlretrieve(url)
            response = json.load(open(data[0], 'r'))
            definition = response['Definition']
            if response['Definition']:
                self.msg(channel, '%s: %s' %
                         (nick, str(response['Definition'])))
            elif response['Answer']:
                self.msg(channel, '%s: %s' %
                         (nick, str(response['Answer'])))
            elif reply_on_notfound:
                self.msg(channel, '%s: Sorry, but I could not find what %s is.' % (nick, param))

    def freebase(self, nick, channel, query, reply_on_notfound = True):
        '''Query Freebase for the query'''
        query = query.replace(' ', '_').replace('what_is_', '')
        data = urllib.urlopen(self.freebase % urllib.quote_plus(query))
        document = json.load(data)
        try:
            description = document['/en/%s' % query]['result']['description']
            self.msg(channel, '%s: %s' % (nick, str(description.split('. ')[0])))
        except Exception, error:
            print document['/en/%s' % query]
            print 'Error: %s, %s' % (error.__repr__(), error.args)
            if reply_on_notfound:
                self.msg(channel, '%s: Sorry, could not find it' % nick)
