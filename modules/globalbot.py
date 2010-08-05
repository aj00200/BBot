import q
import api
import config
class globalbot():
    def go(self,nick,data,channel):
        if api.checkIfSuperUser(data,config.superusers):
            if data.find('?global ')!=-1:
                self.broadcast=data[data.find('?global ')+8:]
                for each in config.autojoin:
                    q.queue.append((each,self.broadcast))
module=globalbot
