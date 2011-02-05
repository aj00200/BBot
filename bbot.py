#! /usr/bin/python
#This Code is licensed under the GNU GPL v3

version='7.0.0b2'
import socket,asyncore
import config,api
if __name__=='__main__':
    api.backend.connect(config.network,config.port,config.ssl)
    asyncore.loop()
