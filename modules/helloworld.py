import q
import api
class module(api.module):
    def privmsg(self,nick,data,channel): #catch privmsgs
	message = data[data.find(' :')+2:]
	if message.lower() == "hello":
		self.msg(channel, "Why, hello there "+nick) #say something to the channel

