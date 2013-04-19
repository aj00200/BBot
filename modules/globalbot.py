'''A module for making global announcements'''
import api
import config


class Module(api.Module):
    '''Send a message to the list of channels the bot joins automatically.'''
    commands = ['global']

    def privmsg(self, nick, data, channel):
        if api.check_if_super_user(data, config.superusers):
            if ':?global ' in data:
                broadcast = data[data.find('global ')+8:]
                for each in config.autojoin:
                    self.msg(each, broadcast)
