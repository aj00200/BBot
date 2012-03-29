'''This module allows channel operators to execute several commands through
BBot, such as kicking, banning, promoting and more. 
It can be used to manage channels on networks without services.'''

import api
import config
class Module(api.Module):
    '''A module to preform channel administration commands'''
    def __init__(self, server = config.network):
        self.blacklist = [] # Load Blacklist
        self.blconfig = open(config.PATH+'trekbot/blacklist', 'r').readlines()
        for each in self.blconfig:
            self.blacklist.append(each.strip('\r\n'))

        self.whitelist = [] # Load Whitelist
        self.wlconfig = open(config.PATH+'trekbot/whitelist', 'r').readlines()
        for each in self.wlconfig:
            self.whitelist.append(each.strip('\r\n'))
        del self.blconfig, self.wlconfig

        # Read config
        self.proxyscan = api.get_config_bool('trekbot', 'proxy-scan')
        self.charybdis = api.get_config_bool('trekbot', 'charybdis-net')

        # New Test Variables
        self.defkickmsg = api.get_config_str('trekbot', 'default-kick-msg')
        self.blacklistkickmsg = api.get_config_str('trekbot', 'blacklist-kick-msg')

        # Setup Variables
        self.pending_bans = {}
        self.pending_unbans = {}
    
        super(Module, self).__init__(server)

        # Hook Superuser Commands
        api.hook_command('op', self.op, server, su = True)
        api.hook_command('deop', self.deop, server, su = True)
        api.hook_command('voice', self.voice, server, su = True)
        api.hook_command('devoice', self.devoice, server, su = True)
        api.hook_command('nick', self.nick, server, su = True)
        api.hook_command('mode', self.mode, server, su = True)
        api.hook_command('echo', self.echo, server, su = True)
        api.hook_command('say', self.echo, server, su = True)
        api.hook_command('me', self.me, server, su = True)
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
        api.hook_command('kickban', self.kick_ban, server, su = True)
        # The following line gives an error when used, it might be better to
        #    make a load_whitelist method and hook a new command for it
        # api.hook_command('rehash_trekbot', self.__init__, server, su = True)
        
        #Defines charybdis only options.
        if (self.charybdis):
            api.hook_command('quiet', self.quiet, server, su = True)
            api.hook_command('unquiet', self.unquiet, server, su = True)
            api.hook_command('protect', self.protect_chan, server, su = True)
            api.hook_command('unprotect', self.unprotect_chan, server, su = True)

    def get_raw(self, raw_type, data):
        if raw_type.lower() == 'code':
            if data[0] == '311': # Whois host line
                nick = data[1].split()[3]
                host = data[1].split()[5]
                if nick in self.pending_bans:
                    for channel in self.pending_bans[nick]:
                        self.mode('*!*@%s' % host, channel, '+b')
                if nick in self.pending_unbans:
                    for channel in self.pending_unbans[nick]:
                        self.mode('*!*@%s' % host, channel, '-b')

    def write_blacklist(self):
        '''Write the blacklist to the harddrive'''
        self.blconfig = open('trekbot/blacklist', 'w')
        for each in self.blacklist:
            self.blconfig.write(each+'\n')

    def write_whitelist(self):
        '''Write the whitelist to the harddrive'''
        self.wlconfig = open('trekbot/whitelist', 'w')
        for each in self.whitelist:
            self.wlconfig.write(each+'\n')

    def get_join(self, nick, user, ip, channel):
        if (ip in self.blacklist):
            self.kick(nick, channel, self.blacklistkickmsg)
        elif (ip in self.whitelist):
            self.mode(nick, channel, '+v')

    def scan(self, ip, channel, nick):
        '''Preform a port scan on an ip address and check for common proxies'''
        scansafe = 1
        try:
            print('Scanning '+ip)
            nm = nmap.PortScanner()
            nm.scan(ip, '808, 23, 1080, 110, 29505, 8080, 3246', '-T5')
            for each in nm.all_hosts():
                print each
                lport = nm[each]['tcp'].keys()
                print lport
                if 808 in lport or 23 in lport or 110 in lport or 1080 in lport or 29505 in lport or 80 in lport or 8080 in lports or 3246 in lports:
                    scansafe = 0
                    print(' * Detected possible drone at: %s' % ip)
            if scansafe:
                self.mode(nick, channel, '+v')
        except:
            print('The port scanner in TrekBot has crashed')

    # Superuser Commands
    def op(self, nick, channel, param = None):
        '''Op a user or yourself; Parameters: (optional) nick'''
        if not param:
            self.mode(nick, channel, '+o')
        else:
            self.mode(param, channel, '+o')

    def deop(self, nick, channel, param = None):
        '''Deop a user or yourself; Parameters: (optional) nick'''
        if not param:
            self.mode(nick, channel, '-o')
        else:
            self.mode(param, channel, '-o')

    def voice(self, nick, channel, param = None):
        '''Voice a user or yourself; Parameters: (optional) nick'''
        if not param:
            self.mode(nick, channel, '+v')
        else:
            self.mode(param, channel, '+v')

    def devoice(self, nick, channel, param = None):
        '''Devoice a user or yourself; Parameters: (optional) nick'''
        if not param:
            self.mode(nick, channel, '-v')
        else:
            self.mode(param, channel, '-v')

    def quiet(self, nick, channel, param = None):
        '''Quiet a user; Parameters: nick'''
        if not param:
            self.msg(channel, '%s: be careful or I will quiet you :P'%nick)
        else:
            self.mode(param, channel, '+q')

    def unquiet(self, nick, channel, param = None):
        '''Unquiet a nick; Parameters: nick'''
        if not param:
            self.mode(nick, channel, '-q')
        else:
            self.mode(param, channel, '-q')

    def nick(self, nick, channel, param = None):
        '''Change to a new nickname; Parameters: new nickname'''
        if not param:
            self.msg(channel, '%s: You need to have a nick following the command'%nick)
        else:
            config.nick = param
            self.raw('NICK %s'%param)

    def set_mode(self, nick, channel, param = None):
        '''Set a mode on the channel; Parameters: mode string (like "+o bbot")'''
        if not param:
            self.msg(channel, '%s: You need to tell me what modes to set' % nick)
        else:
            self.mode('', channel, param)

    def echo(self, nick, channel, param = None):
        '''Say what the parmeter is; Parameters: a string to say'''
        if not param:
            self.msg(channel, '%s: I can\'t echo nothing' % nick)
        else:
            self.msg(channel, param)

    def me(self, nick, channel, param = None):
        '''Say the parameter as an ACTION; Parameters: a string to say'''
        if not param:
            self.msg(channel, '%s: I need an action to preform.' % nick)
        else:
            self.msg(channel, '\x01ACTION %s\x01' % param)

    def set_topic(self, nick, channel, param = None):
        '''Set the topic in the channel; Parameters: a topic string'''
        if not param:
            self.msg(channel, '%s: You need to specify a topic' % nick)
        else:
            self.raw('TOPIC %s :%s'%(channel, param))

    def set_ban(self, nick, channel, param = None):
        '''Set a ban on a user's host; Parameters: nick'''
        if not param:
            self.msg(channel, '%s: You need to specify who to ban' % nick)
        else:
            if '!' in param:
                self.mode(param, channel, '+b')
                return
            elif param in self.pending_bans:
                self.pending_bans[param].append(channel)
            else:
                self.pending_bans[param] = [channel]
            self.raw('WHOIS %s' % param)

    def del_ban(self, nick, channel, param = None):
        '''Unban a user's host; Parameters: nick'''
        if not param:
            self.msg(channel, '%s: You need to specify who to unban' % nick)
        else:
            if '!' in param:
                self.mode(param, channel, '-b')
                return
            elif param  in self.pending_unbans:
                self.pending_unbans[param].append(channel)
            else:
                self.pending_unbans[param] = [channel]
            self.raw('WHOIS %s' % param)

    def kick_user(self, nick, channel, param = None):
        '''Kick a user from a channel; Parameters: nick'''
        if not param:
            self.msg(channel, '%s: You need to tell me who to kick' % nick)
        else:
            message = ''
            if ' ' in param.strip(' '):
                message = param[param.find(' ')+1:]
                param = param[:param.find(' ')]
            else:
                message = self.defkickmsg % nick
            self.kick(param, channel, message)

    def invite_user(self, nick, channel, param = None):
        '''Invite a user to a channel; Parameters: nick'''
        if not param:
            self.msg(channel, '%s: You need to tell me who to invite!'%nick)
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

    def kick_ban(self, nick, channel, param = None):
        '''Kickban a user; parameters: nick'''
        if not param:
            self.msg(channel, '%s: You need to specify a target' % nick)
        else:
            #Begin code for banning.
            if param  in self.pending_unbans:
                self.pending_bans[param].append(channel)
            else:
                self.pending_bans[param] = [channel]
            self.raw('WHOIS %s' % param)
            #Begin code for kick
            message = 'You have  been kicked from the channel.  (requested by %s)' % nick
            self.kick(param, channel, message)

    def protect_chan(self, nick, channel, param = None):
        '''On charybdis-based networks with services integration with bans, initiates the command /mode channel +q $~a'''
        self.mode('', channel, '+q $~a')

    def unprotect_chan(self, nick, channel, param = None):
        '''On charybdis-based networks with services integration with bans, initiates the command /mode channel -q $~a'''
        self.mode('', channel, '-q $~a')

    #Blacklist/Whitelist Commands - SuperUser Only
    def blacklist_list(self, nick, channel, param = None):
        '''PMs the caller the list of blacklisted hosts'''
        self.msg(nick, str(self.blacklist))

    def blacklist_add(self, nick, channel, param = None):
        '''Adds a host to the blacklist'''
        if not param in self.blacklist:
            self.blacklist.append(param)
            self.write_blacklist()
        else:
            self.msg(nick, 'That host is already blacklisted.')

    def blacklist_del(self, nick, channel, param = None):
        '''Removes a host from the blacklist'''
        if param in self.blacklist:
            self.blacklist.pop(self.blacklist.index(param))
            self.write_blacklist()
        else:
            self.msg(nick, 'That host is not blacklisted.')

    def whitelist_list(self, nick, channel, param = None):
        '''PMs the caller the list of whitelisted hosts'''
        self.msg(nick, str(self.whitelist))

    def whitelist_add(self, nick, channel, param = None):
        '''Adds a host to the whitelist'''
        if not param:
            self.msg(channel, '%s: You need to specify something to add to the whitelist.'%nick)
        else:
            if not param in self.whitelist:
                self.whitelist.append(param)
                self.write_whitelist()
            else:
                self.msg(nick, 'That host is already whitelisted.')

    def whitelist_del(self, nick, channel, param = None):
        '''Deletes a host from the whitelist'''
        if not param:
            self.msg(channel, '%s: You need to specify something to remove from the whitelist.'%nick)
        else:
            if param in self.whitelist:
                self.whitelist.pop(self.whitelist.index(param))
                self.write_whitelist()
            else:
                self.msg(nick, 'That host is not whitelisted.')
