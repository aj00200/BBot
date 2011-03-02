import q, re, api
class Module(api.module):
    '''A module for matching regular expressions and
    forwarding the data to a nick or channel'''
    commands = ['grepfwd']
    def __init__(self, server):
        self.fwds = {}
        api.module.__init__(self, server)
    def privmsg(self, nick, data, channel):
        for each in self.fwds:
            if re.search(each, data):
                self.append((self.fwds[each], data))
    def grepfwd(self, nick, channel, param = None):
        if ' > ' in message:
            self.add_fwd(message)
    def add_fwd(self, data):
        query = param.split(' > ')
        self.fwds[query[0]] = query[1]
