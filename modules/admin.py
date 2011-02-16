import re,api,time,config,thread,colorz,sqlite3
reportchan = "#mithos-ctl"
class module(api.module):
	def privmsg(self,nick,data,channel):
		if api.check_if_super_user(data) == True:
			ldata=data.lower()
			msgl=ldata[ldata.find(' :')+2:]
			msg=data[data.find(' :')+2:]
			if "raw" in msgl:
				#self.msg("#bikcmp",api.check_if_super_user(data))
				rawmsg = msg.split("raw ")[1]
				self.msg(reportchan,data)
				self.raw(rawmsg)
			elif "$join" in msgl:
				joinchan=msg.split("join ")[1]
				self.msg(reportchan,data)
				self.raw("JOIN "+joinchan)
			elif "$part" in msgl:
				partchan=msg.split("part ")[1]
				self.msg(reportchan,data)
				self.raw("PART "+partchan+" :Requested by "+nick)			
				
			
		
			
