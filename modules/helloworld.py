import q
import api
class module(api.module):
    def privmsg(self,nick,data,channel): #catch privmsgs
      try: #if it can't split the message, ignore the error
        message = data[data.find(' :')+2:]
        if message.lower() == "hello":
            self.msg(channel, "Why, hello there "+nick) #say something to the channel
            self.raw("PRIVMSG "+channel+" :I said something via self.raw!") #send something via api.raw()
            
      except: #if I can't split up the message, or something goes wrong, don't do anything
          pass 
    def join(self,nick,user,host,channel): #Get joins from async.py
        self.msg(channel, "NICK: "+nick+" USER: "+user+" HOST: "+host)
