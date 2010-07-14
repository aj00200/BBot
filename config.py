config=open('config','r')
cline=config.readline()
mynick=cline.split('nick: ')[-1][0:-1]
cline=config.readline()
username=cline.split('username: ')[-1][0:-1]
cline=config.readline()
password=cline.split('password: ')[-1][0:-1]
cline=config.readline()
network=cline.split('network: ')[-1][0:-1]
cline=config.readline()
port=int(cline.split('port: ')[-1].strip())
print('Connecting to: %s' % network)

cline=config.readline()
autojoin=cline.split('channels: ')[-1].split(' ')
cline=config.readline()
superusers=cline.split('super-user: ')[-1].split(' ')

cline=config.readline()
sleep_after_join=float(cline.split('wait-after-identify: ')[-1].strip())
cline=config.readline()
wait_recv=int(cline[cline.find(' '):].strip('\r\n'))
cline=config.readline()
cmd_char=cline[cline.find(' '):].strip('\r\n')
