'''This module implements flood control and anti-spam measures.'''
import re
import time
import thread

import api
import config

class Module(api.Module):
    def __init__(self, server):
        super(Module, self).__init__(server)

        # Hook Commands
        api.hook_command(';', self.set_spam_string, server, su = True)

        # Load/Set Settings
        self.hilight_limit = api.get_config_int('BlockBot', 'highlight-limit')
        findlist = api.get_config_str('BlockBot', 'spam-strings')
        self.mps_limit = api.get_config_float('BlockBot', 'mps-limit')
        self.storage_time = 25
        self.repeat_limit = 3
        self.repeat_1word = 4
        self.blacklistkickmsg = api.get_config_str('BlockBot','blacklist-kick-msg')
        self.floodkickmsg = api.get_config_str('BlockBot', 'flood-kick-msg')
        self.repeatkickmsg = api.get_config_str('BlockBot', 'repeat-kick-msg')
        self.masspingkickmsg = api.get_config_str('BlockBot', 'mass-ping-kick-msg')

        # Compile Spam Strings        
        self.findlist = []
        if findlist:
            for each in findlist.split('^^^@@@^^^'):
                self.findlist.append(re.compile(each))

        # Load Default Data
        self.msglist = []
        self.nicklists = {}
        self.lastnot = ('BBot', time.time(), '')

    def privmsg(self, nick, data, channel):
        '''Check messages for spam'''
        self.msglist.insert(0, (nick, channel,
                                api.get_message(data), time.time()))

        if not api.check_if_super_user(data, config.superusers):
            # Check for spam strings
            ldata = data.lower()
            for each in self.findlist:
                if re.search(each, ldata):
                    self.kick(nick, channel, self.blacklistkickmsg)
                    return

            # Extract messages by this user
            user_msgs = []
            for msg in self.msglist:
                if msg[0] == nick:
                    user_msgs.append((nick, msg[1], msg[2], msg[3]))

            # Check for flooding
            if len(user_msgs) > 2 and self.get_mps(user_msgs) > self.mps_limit:
                self.kick(nick, channel, self.floodkickmsg)
                self.msglist.pop(0)

            # Check for repeats
            strings = []
            repeats = 0
            for msg in user_msgs:
                if msg[2] not in strings:
                    strings.append(msg[2])
                else:
                    repeats += 1
            if repeats > self.repeat_limit-1:
                self.kick(nick, channel, self.repeatkickmsg)
                self.msglist.pop(0)

            # Clear out old messages
            now = time.time()
            for msg in self.msglist:
                if now - msg[3] > self.storage_time:
                    self.msglist.remove(msg)

            # Check for highlights
            thread.start_new_thread(self.check_hilight, (nick, data, channel))

    def get_mps(self, user_msgs):
        '''Count the number of messages sent per second'''
        time_range = user_msgs[0][3] - user_msgs[-1][3]
        mps =  len(user_msgs) / time_range
        return mps
                

    def check_hilight(self, nick, data, channel):
        '''Check if nick has pinged more than self.hilight_limit people, and if so, kick them'''
        ldata = data[data.find(' :')+2:].lower()
        if channel not in self.nicklists:
            self.nicklists[channel] = [nick.lower()]

        found = 0
        for each in self.nicklists[channel]:
            if each in ldata:
                found += 1
        if found > self.hilight_limit:
            print '* kicking %s out of %s' % (nick, channel)
            self.kick(nick, channel, self.masspingkickmsg)

    def get_join(self, nick, user, host, channel):
        '''Add user to nicklist, and preform optional proxy scan'''
        if channel in self.nicklists and nick not in self.nicklists[channel]:
            self.nicklists[channel].append(nick)
        else:
            self.nicklists[channel] = [nick]

    def get_notice(self, nick, channel, data):
        # Add notice to the message lsit
        self.msglist.insert(0, (nick, channel, api.get_message(data), time.time()))

        # Check notice for spam strings
        for each in self.findlist:
            if re.search(each, data):
                self.kick(nick, channel, 'You have matched a spam string and have been banned. If this was a mistake, please contact a channel op to get unbanned')
                self.mode(nick, channel, '+b')

    def get_raw(self, type, data):
        if type == 'PART' or type == 'KICK': # Kick or Part
            try:
                if data[0] in self.nicklists[data[2]]:
                    self.nicklists[data[2]].pop(self.nicklists[data[2]].index(data[0]))
            except Exception:
                pass
        elif type == 'QUIT': # Quit
            try:
                for channel in self.nicklists:
                    if data[0] in self.nicklists[channel]:
                        self.nicklists[channel].pop(self.nicklists[channel].index(data[0]))
            except Exception:
                pass

        elif type == 'CODE' and data[0] == '353':
            channel = data[1][data[1].find(' = ')+3:data[1].find(' :')]
            names = data[1][data[1].find(' :')+2:].split()
            safe_names = []
            for each in names:
                safe_names.append(each.strip('@+%~').lower())
            if channel not in self.nicklists:
                self.nicklists[channel] = []
            for each in safe_names:
                self.nicklists[channel].append(each)

    # Supueruser Commands
    def set_spam_string(self, nick, channel, param = None):
        '''Set a spam string to automatically kick on'''
        if param:
            try:
                self.findlist.append(re.compile(param))
                self.msg(channel, '%s: string blacklisted' % nick)
            except Exception:
                self.msg(channel, '%s: error banning string' % nick)
