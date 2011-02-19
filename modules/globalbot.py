import api,config
class module(api.module):
    commands=['global']
    def __init__(self,server):
        api.module.__init__(self,server)
    def privmsg(self,nick,data,channel):
        if api.check_if_super_user(data,config.superusers) and ':?global ' in data:
            self.broadcast=data[data.find('global ')+8:]
            for each in config.autojoin:
                self.msg(each,self.broadcast)
