import q, re, api
class module(api.module):
    commands = ['grepfwd']
    def __init__(self, server):
        self.fwds = {}
        api.module.__init__(self, server)
    def privmsg(self, nick, data, channel):
        if ':?grepfwd' in data and ' > ' in data and api.check_if_super_user(data):
            self.add_fwd(data)
        if ':?grepfwd help' in data:
            self.append((channel, '%s: The ?grepfwd command allows you to add a regular expression, which, when found in a messsage, will cause the message to be passed on. Syntax: ?grepfwd <expression> > <nick or chan>'%nick))
        for each in self.fwds:
            if re.search(each, data):
                self.append((self.fwds[each], data))
    def add_fwd(self, data):
        query = data[data.find(':?grepfwd ')+10:].split(' > ')
        self.fwds[query[0]] = query[1]
