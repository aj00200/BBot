"""This module allows channel operators to execute several commands through BBot, such as kicking, banning, 
promoting and more. It can be used to manage channels on networks without services, such as EFnet."""

import api, config
class Module(api.module):
    def __init__(self, server = config.network):
        self.blacklist = []
        self.blconfig = open('trekbot/blacklist', 'r').readlines()
        for each in self.blconfig:
            self.blacklist.append(each.strip('\r\n'))
        self.whitelist = []
        self.wlconfig = open('trekbot/whitelist', 'r').readlines()
        for each in self.wlconfig:
            self.whitelist.append(each.strip('\r\n'))
        del self.blconfig, self.wlconfig
        self.proxyscan = api.get_config_bool('trekbot', 'proxy-scan')
        api.module.__init__(self, server)

        # Hook Superuser Commands
        api.hook_command('op', self.op, server, su = True)
        api.hook_command('deop', self.deop, server, su = True)
        api.hook_command('voice', self.voice, server, su = True)
        api.hook_command('devoice', self.devoice, server, su = True)
        api.hook_command('quiet', self.quiet, server, su = True)
        api.hook_command('unquiet', self.unquiet, server, su = True)
        api.hook_command('nick', self.nick, server, su = True)
        api.hook_command('mode', self.mode, server, su = True)
        api.hook_command('echo', self.echo, server, su = True)
        api.hook_command('say', self.echo, server, su = True)
        api.hook_command('topic', self.set_topic, server, su = True)
        api.hook_command('ban', self.set_ban, server, su = True)
        api.hook_command('unban', self.del_ban, server, su = True)
        api.hook_command('listbl', self.blacklist_list, server, su = True)
        api.hook_command('blacklist', self.blacklist_add, server, su = True)
        api.hook_command('unblacklist', self.blacklist_del, server, su = True)
        api.hook_command('listwl', self.whitelist_list, server, su = True)
        api.hook_command('whitelist', self.whitelist_add, server, su = True)
        api.hook_command('unwhitelist', self.whitelist_del, server, su = True)
        api.hook_command('kick', self.kick_user, server, su = True)
        api.hook_command('invite', self.invite_user, server, su = True)
        api.hook_command('rehash_trekbot', self.__init__, server, su = True)

    def write_blacklist(self):
        self.blconfig = open('trekbot/blacklist', 'w')
        for each in self.blacklist:
            self.blconfig.write(each+'\n')

    def write_whitelist(self):
        self.wlconfig = open('trekbot/whitelist', 'w')
        for each in self.whitelist:
            self.wlconfig.write(each+'\n')

    def get_join(self, nick, user, ip, channel):
        if (ip in self.blacklist):
            self.kick(nick,channel,'You are on the blacklist')
        elif (ip in self.whitelist):
            self.mode(nick,channel,'+v')

    def scan(self, ip, channel, nick):
        self.scansafe = 1
        try:
            print('Scanning '+ip)
            self.nm = nmap.PortScanner()
            #80, 8080, 1080, 3246
            self.nm.scan(ip, '808, 23, 1080, 110, 29505, 8080, 3246', '-T5')
            for each in nm.all_hosts():
                print each+':::'
                lport = nm[each]['tcp'].keys()
                print lport
                if 808 in lport or 23 in lport or 110 in lport or 1080 in lport or 29505 in lport or 80 in lport or 8080 in lports or 3246 in lports:
                    self.scansafe = 0
                    print(' * Detected possible drone at: %s' % ip)
            del self.nm
            if self.scansafe:
                self.mode(nick, channel, '+v')
        except:
            print('The port scanner in TrekBot has crashed')

    # Superuser Commands
    def op(self, nick, channel, param = None):
        if not param:
            self.mode(nick, channel, '+o')
        else:
            self.mode(param, channel, '+o')

    def deop(self, nick, channel, param = None):
        if not param:
            self.mode(nick, channel, '-o')
        else:
            self.mode(param, channel, '-o')

    def voice(self, nick, channel, param = None):
        if not param:
            self.mode(nick, channel, '+v')
        else:
            self.mode(param, channel, '+v')

    def devoice(self, nick, channel, param = None):
        if not param:
            self.mode(nick, channel, '-v')
        else:
            self.mode(param, channel, '-v')

    def quiet(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: be careful or I will quiet you :P'%nick)
        else:
            self.mode(param, channel, '+q')

    def unquiet(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to tell me what to unquiet.  I can\'t unquiet [NULL]!'%nick)
        else:
            self.mode(param, channel, '-q')

    def nick(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to have a nick following the command'%nick)
        else:
            config.nick = param
            self.raw('NICK %s'%param)

    def set_mode(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to tell me what modes to set'%nick)
        else:
            self.mode('', channel, param)

    def echo(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: I can\'t echo nothing'%nick)
        else:
            self.msg(channel, param)

    def set_topic(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to specify a topic'%nick)
        else:
            self.raw('TOPIC %s :%s'%(channel, param))

    def set_ban(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to specify what to ban'%nick)
        else:
            self.mode(param, channel, '+b')

    def del_ban(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to specify what to unban'%nick)
        else:
            self.mode(param, channel, '-b')

    def kick_user(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to tell me who to kick'%nick)
        else:
            message = ''
            if ' ' in param.strip(' '):
                message = param[param.find(' ')+1:]
                param = param[:param.find(' ')]
            else:
                message = 'You have been kicked from the channel.  (requested by %s)'%nick
            self.kick(param, channel, message)

    def invite_user(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to give me parameters for me to invite a user!'%nick)
        else:
            targetchan = ''
            targetuser = ''
            if ' ' in param:
                targetchan = param[param.find(' ')+1:]
                targetuser = param[:param.find(' ')]
            else:
                targetchan = channel
                targetuser = param
            self.raw('INVITE %s :%s'%(targetuser, targetchan))

    #Blacklist/Whitelist Commands - SuperUser Only
    def blacklist_list(self, nick, channel, param = None):
        self.msg(nick, str(self.blacklist))

    def blacklist_add(self, nick, channel, param = None):
        if not param in self.blacklist:
            self.blacklist.append(param)
            self.write_blacklist()
        else:
            self.msg(nick, 'That host is already blacklisted.')

    def blacklist_del(self, nick, channel, param = None):
        if param in self.blacklist:
            self.blacklist.pop(self.blacklist.index(param))
            self.write_blacklist()
        else:
            self.msg(nick, 'That host is not blacklisted.')

    def whitelist_list(self, nick, channel, param = None):
        self.msg(nick, str(self.whitelist))

    def whitelist_add(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to specify something to add to the whitelist.'%nick)
        else:
            if not param in self.whitelist:
                self.whitelist.append(param)
                self.write_whitelist()
            else:
                self.msg(nick, 'That host is already whitelisted.')
    def whitelist_del(self, nick, channel, param = None):
        if not param:
            self.msg(channel, '%s: You need to specify something to remove from the whitelist.'%nick)
        else:
            if param in self.whitelist:
                self.whitelist.pop(self.whitelist.index(param))
                self.write_whitelist()
            else:
                self.msg(nick, 'That host is not whitelisted.')
