import q
import api
class module(api.module):
    def privmsg(self,nick,data,channel): #catch privmsgs
	  try: #if it can't split the message, ignore the error
		message = data.split("PRIVMSG "+channel+" :")[1]
		if message.lower() == "hello":
			self.msg(channel, "Why, hello there "+nick) #say something to the channel
			
	  except: #if I can't split up the message, or something goes wrong, don't do anything
		  pass 
