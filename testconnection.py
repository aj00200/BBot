
import socket
import thread
import time
serv=socket.socket()
serv.bind(('127.0.01',6667))

def server():
    serv.listen(2)
    conn=serv.accept()[0]
    while 1:
        data=conn.recv(256)
        print data
        if data.find('USER')!=-1:
            user=data.split()[3]
            conn.send('PING :12345\r\n')
            break
    while 1:
        data=conn.recv(64)
        print data
        if data.find('PONG :12345')!=-1:
            conn.send(':127.0.0.1 %s 001 :Welcome to the GNU Net!\r\n'%user)
            conn.send(':127.0.0.1 %s Your host is 127.0.0.1 Running AJ00200 Serv\r\n'%user)
            conn.send(':127.0.0.1 %s This server was created at none of your busniess oclock\r\n'%user)
            conn.send(':127.0.0.1:%s 375 :NICK\r\n'%user)
            conn.send(':127.0.0.1 %s 372 :Welcome!\r\n'%user)
            conn.send(':%s MODE %s :+i\r\n'%(user,user))
            break
    while 1:
        data=conn.recv(512)
        time.sleep(5)
        conn.send('PING :123123123\r\n')
        time.sleep(1)
        conn.send(':aj!aj@aj00200/rulez PRIVMSG #bots :?hi\r\n')
        if data.find('JOIN ')!=-1:
            conn.send('JOIN %s'%data[data.find('JOIN ')+5:])
thread.start_new_thread(server,())
time.sleep(60)
#mport bbot
