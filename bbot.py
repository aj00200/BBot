#! /usr/bin/python
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='5.2.1'
import q,config,sys,re,time,thread,colorz,traceback,api,asyncore
sys.path.insert(1,'%s/libs'%sys.path[0])
sys.path.insert(0,'%s/modules'%sys.path[0])

networks={config.network: []}
module_list=api.getConfigStr('main','modules').split()
for module in module_list:
	globals()[module]=__import__(module)
	networks[config.network].append(eval(module+'.module(config.network)'))
def add_network(name):
	'''Connect to a new network'''
	print colorz.encode('Adding Network "%s"'%name,'yellow')
	networks[name]=[BBot.module(name)]
def load_module(name,server):
	'''Loads the module called name for the server, server. Returns True if sucessful and False if it fails. Will also report the error in the error channel'''
	print colorz.encode('Loading module "%s" for server "%s"'%(name,server),'yellow')
	try:
		globals()[name]=__import__(name)
		networks[server].append(eval(name).module(server))
		return True
	except Exception,e:
		q.append(config.network,((config.error_chan,'BBot has crashed with error: %s; and args: %s'%(type(e),e.args)))) 
		return False
def reload_module(name,server):
	try:
		for each in networks[server]:
			if isinstance(each,eval(name+'.module')):
				each.__destroy__()
				networks[server].pop(networks[server].index(each))
				reload(eval(name))
				networks[server].append(eval(name+'.module("%s")'%config.network))
				break
	except Exception,e:
		q.append(config.network,(config.error_chan,'Traceback: %s'%traceback.format_exc().replace('\n',' -- ')))
lastloop=time.time()-10
def loop():
	'''	Calls the loop() method of each module every 5 seconds + execution time	'''
	try:
		time.sleep(5)
		for network in networks:
			for module in networks[network]:
				module.loop()
	except Exception,e:
		q.append(config.network,((config.error_chan,'<<BBot system error "bbot.py - loop()" with error: %s; args %s'%(type(e),e.args))))
	thread.start_new_thread(loop,())
def start_bot():
	thread.start_new_thread(loop,())
	import q
	asyncore.loop()
if __name__ == '__main__':
	start_bot()

