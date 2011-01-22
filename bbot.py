#! /usr/bin/python
#This Code is licensed under the GNU GPL v3

version='6.0.1'
import socket,asyncore
import config,api
if __name__=='__main__':
    backend = getattr(__import__('backends.async'),'async')
    backend.connect(config.network,config.port,False)
    asyncore.loop()
