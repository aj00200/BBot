#! /usr/bin/python
#This Bot is licensed under the GNU GPL v3

version='6.0.0'
import socket,asyncore
import cProfile
if __name__=='__main__':
    backend = getattr(__import__('backends.async'),'async')
    backend.connect('irc.fossnet.info',6667,False)
    asyncore.loop()
