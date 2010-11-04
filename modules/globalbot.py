import q,api,config
class module(api.module):
    commands=['global']
    def __init__(self,server):
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        if api.checkIfSuperUser(data,config.superusers) and ':?global ' in data:
            self.broadcast=data[data.find('?global ')+8:]
            for each in config.autojoin:
                self.append((each,self.broadcast))
