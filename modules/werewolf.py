"""This module is an IRC implementation of the Werewolf (a.k.a. Mafia) RPG party game
<http://en.wikipedia.org/wiki/Mafia_(party_game)>."""

import thread
import time
import api

import config
import libs.wolflib

class Module(api.module):
    def __init__(self, address):
        api.module.__init__(self, address)        
        self.game = {
            'phase':'waiting', 
            'main_channel':api.get_config_str('werewolf', 'main-channel'), 
            'wolf_channel':api.get_config_str('werewolf', 'wolf-channel'), 
            'seer_channel':api.get_config_str('werewolf', 'seer-channel'), 
            'players':{}, 
            'roles':{}, 

            'killvotes':{}, 
            'killvoters':[]
        }
        self.waiting = []
        self.commands = {
            'join':self.join_game, 
            'role':self.role, 
            'kill':self.kill
        }
        self.su_commands = {
            'start':self.start_game, 
            'lkill':self.lkill
        }
    def privmsg(self, nick, data, channel):
        if ' :%sw.'%config.cmd_char in data:
            command = data[data.find(' :%sw.'%config.cmd_char)+4+len(config.cmd_char):]
            params = ''
            if ' ' in command:
                params = command[command.find(' ')+1:]
                command = command[:command.find(' ')]
            if command in self.commands:
                self.commands[command](nick, channel, params)
            elif api.check_if_super_user(data) and command in self.su_commands:
                self.su_commands[command](nick, channel, params)
    # Public Commands
    def join_game(self, nick, channel, params = None):
        if self.game['phase'] ==  'waiting':
            self.notice(self.game['main_channel'], '<< %s has joined the game! >>'%nick)
            self.game['players'][nick] = None
        else:
            self.msg(channel, '%s: Please wait for the next game'%nick)
    def role(self, nick, channel, params = None):
        self.msg(nick, 'Thanks, the game will begin shortly')
        self.game['roles'][nick] = params
    def kill(self, nick, channel, params = None):
        if (nick in self.game['killvoters']):
                return
        if (channel ==  self.game['wolf_channel']) and (self.game['phase'] ==  'night'):
            if (params in self.game['killvotes']):
                self.game['killvotes'][params]+= 1
            else:
                self.game['killvotes'][params] = 1
        self.game['killvoters'].append(nick)
    # Super User Commands
    def start_game(self, nick, channel, params = None):
        if (self.game['phase'] ==  'waiting'):
            self.game['phase'] = 'asigning'
            self.notice(self.game['main_channel'], '<< Assigning Roles >>')
            self.randomize_roles()
            self.notice(self.game['main_channel'], '<< Sending Invites >>')
            libs.wolflib.send_invites(self)
            self.mode('', self.game['main_channel'], '+mz')
            self.game['phase'] = 'intro'
            self.notice(self.game['main_channel'], '<< Please Describe your role in a PM to me; *Syntax:* %sw.role <your role> >>'%config.cmd_char)
            self.notice(self.game['main_channel'], '<< The game begins in 60 seconds >>')
            thread.start_new_thread(self.start_game_in_60, ())
    def lkill(self, nick, channel, params = None):
        if (self.game['phase'] == 'night'):
            self.msg(channel, '%s: %s'%(nick, self.game['killvotes']))
    # Internal Methods
    def randomize_roles(self):
        self.wolves = 0
        self.seers = 0
        self.villagers = 0
        for player in self.game['players']:
            if (self.wolves<2):
                self.game['players'][player] = 'wolf'
            elif (self.seers == 0):
                self.game['players'][player] = 'seer'
            else: # Decide at random
                r = random.randint(0, 5)
                if r < 4:
                    self.game['players'][player] = 'villager'
                elif r ==  5:
                    self.game['players'][player] = 'wolf'

    def invite(self, player, channel):
        self.raw('INVITE %s %s'%(player, channel))
        
    def start_game_in_60(self):
        time.sleep(60)
        for player in self.game['roles']:
            self.msg(self.game['main_channel'], ' --> %s is a %s'%(player, self.game['roles'][player]))
        self.game['phase'] = 'night'
        libs.wolflib.night_phase(self)
    def total_kill_votes(self):
        max_votes = 0
        max_player = None
        for person in self.game['killvotes']:
            if (self.game['killvotes'][person] > max_votes):
                max_votes = self.game['killvotes'][person]
                max_player = player
        if (max_player):
            self.notice(self.game['main_channel'], '<< The villages awake to find the body of %s >>'%max_player)
            self.mode(self.game['main_channel'], max_player, '-v')
            if (self.game['players'][max_player] ==  'wolf'):
                self.kick(self.game['wolf_channel'], max_player, 'You have died')
            elif (self.game['players'][max_player] ==  'seer'):
                self.kick(self.game['seer_channel'], max_player, 'You have died')
