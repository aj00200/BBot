"""This module allows users to set a status that others can query."""

import api, config, time, thread
class module(api.module):
    commands = ['status', 'whereis', 'notify', 'timer', 'rawtimer']
    def __init__(self, server):
        self.statuses = {}
        api.module.__init__(self, server)
    def privmsg(self, nick, data, channel):
        if ':%sstatus '%config.cmd_char in data:
            words = data[data.find('status ')+7:]
            self.statuses[nick.lower()] = words
        elif 'whereis' in data:
            who = data[data.find('whereis ')+8:].strip(' ')
            if who.lower() in self.statuses:
                self.msg(channel, '%s: %s\'s status is: %s'%(nick, who, self.statuses[who.lower()]))
        if api.check_if_super_user(data):
            if '%stimer'%config.cmd_char in data:
                words = data[data.find('timer ')+6:]
                words = words.split('m ', 1)
                thread.start_new_thread(self.timer, (words[0], 'PRIVMSG %s :%s'%(channel, words[1])))
            elif '%srawtimer '%config.cmd_char in data:
                words = data[data.find('rawtimer ')+9:]
                words = words.split('m ', 1)
                thread.start_new_thread(self.timer, (words[0], words[1]))
    def timer(self, wait, message):
        time.sleep(float(wait)*60)
        self.raw(message)
