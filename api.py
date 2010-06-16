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
