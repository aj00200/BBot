import ConfigParser,re
c=ConfigParser.ConfigParser()
f=open('config','r')
c.readfp(f)
nick=c.get('main','nick')
username=c.get('main','username')
password=c.get('main','password')
network=c.get('main','network')
port=c.getint('main','port')
autojoin=c.get('main','channels').split()
modules=c.get('main','modules').split()
superusers=c.get('main','super-users').split()
sleep_after_id=c.getfloat('main','wait-after-identify')
wait_recv=c.getint('main','read-wait')
cmd_char=c.get('main','command-char')
error_chan=c.get('main','report-error')
allow_invite=c.get('main','allow-invite')
ignore=re.compile(c.get('main','ignore-re'))
