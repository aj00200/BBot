"""This module is an IRC implementation of the Werewolf (a.k.a. Mafia)
 RPG party game <http://en.wikipedia.org/wiki/Mafia_(party_game)>."""

import thread
import time
import api

import config
import libs.wolflib

class Module(api.module):
    def __init__(self, address):
        api.module.__init__(self, address)        
        self.vars = {
            'main_channel':api.get_config_str('werewolf', 'main-channel'), 
            'wolf_channel':api.get_config_str('werewolf', 'wolf-channel'), 
            'seer_channel':api.get_config_str('werewolf', 'seer-channel'), 
        }
        # Setup type counts
        self.seers = 0
        self.wolves = 0
        self.villagers = 0

        # Manage players
        self.players = {}
        self.waiting = []

        # Setup state
        self.phase = 'waiting'
