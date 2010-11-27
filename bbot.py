#! /usr/bin/python
#This Bot is licensed under the GNU GPL v3

version='6.0.0'
import socket,asyncore
if __name__=='__main__':
    import backends.async as backend
    backend.connect('irc.fossnet.info',6667,False)
    asyncore.loop()
