import re
import api


class Module(api.Module):
    '''A module for matching regular expressions and
    forwarding the data to a nick or channel'''
    def __init__(self, server):
        super(Module, self).__init__(server)
        api.hook_command('grepfwd', self.grepfwd, server, su = True)
        self.fwds = {}

    def privmsg(self, nick, data, channel):
        for each in self.fwds:
            if re.search(each, data):
                self.msg(self.fwds[each], data)

    def grepfwd(self, nick, channel, param = None):
        if param and ' > ' in param:
            self.add_fwd(param)

    def add_fwd(self, param):
        query = param.split(' > ')
        self.fwds[query[0]] = query[1]
