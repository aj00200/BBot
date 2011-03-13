import api
import config

class Module(api.Module):
    '''A module for making global announcements'''
    commands = ['global']

    def privmsg(self, nick, data, channel):
        if api.check_if_super_user(data, config.superusers):
            if ':?global ' in data:
                self.broadcast = data[data.find('global ')+8:]
                for each in config.autojoin:
                    self.msg(each, self.broadcast)
