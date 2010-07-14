import q
def getHost(data):
    host=data[data.find('@')+1:data.find('PRIVMSG')]
    return host
def checkIfSuperUser(data,superusers):
    host=getHost(data)
    for su in superusers:
        if host.find(su)!=-1:
            return True
    else:
        return False
def pong(data):
    if data.find ('PING')!=-1:
        print('PING RECEIVED')
        q.queue.raw('PONG '+data.split()[ 1 ]+'\r\n') #Return the PING to the server
        print('PONGING')