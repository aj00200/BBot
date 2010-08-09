import q
import api
import config
class globalbot(api.module):
    def __init__(self,server):
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        if api.checkIfSuperUser(data,config.superusers):
            if data.find('?global ')!=-1:
                self.broadcast=data[data.find('?global ')+8:]
                for each in config.autojoin:
                    self.append((each,self.broadcast))
module=globalbot
