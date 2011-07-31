import re
import api
import config

try:
    import json
    factoids = open(config.PATH + 'database.json')
    dict = json.load(factoids)
    del factoids
except:
    print(' * Could not load the factoid file')
    dict = {}


class Module(api.Module):
    stop_words = [
        ' a ', ' the ', ' was ', ' an '
    ]
    is_words = [
        ' was ', ' are ', ' am '
    ]

    def __init__(self, address):
        super(Module, self).__init__(address)
        self.command_list = []
        self.command_start = ':'+config.cmd_char
        self.cmd_len = len(self.command_start)

        # Hook commands
        api.hook_command('writedb', self.su_writedb, address, su = True)
        api.hook_command('add', self.su_add, address, su = True)
        api.hook_command('del', self.su_del, address, su = True)

    def privmsg(self, nick, data, channel):
        if '#' not in channel: # if message is a pm                             
            channel = nick
        ldata = data.lower()

        # Check if message is a command                                        
        if self.command_start in data:
            cmd = data[data.find(self.command_start)+len(self.command_start):]
            if ' ' in cmd:
                cmd = cmd[:cmd.find(' ')]

            # Superuser Commands                                                
            if api.check_if_super_user(data):
                if ' > ' in data:
                    channel = data[data.find(' > ')+3:]
                    data = data[:data.find(' > ')]

            # Normal Commands                                                   
            cmd = data[data.find(self.command_start)+self.cmd_len:]
            if ' | ' in cmd:
                nick = cmd[cmd.find(' | ')+3:]
                cmd = cmd[:cmd.find(' | ')]
            self.query(cmd, nick, channel)

        # Check if I've been pinged                                                                                                                                       
        if (' :%s: '%config.nick.lower() in ldata) or (' :%s, '%config.nick.lower() in ldata):
            msg = api.get_message(data).lower()
            q = msg[msg.find(config.nick.lower())+len(config.nick.lower())+2:]
            self.query(q, nick, channel)

        # Answer basic questions                                                                                                                                          
        ldata = ldata.replace('whats', 'what is')
        if re.search('(what|where|who) (is|was|are|am)', ldata):
            for word in self.stop_words:
                ldata = ldata.replace(word, ' ')
            for word in self.is_words:
                ldata = ldata.replace(word, ' is ')
            q = ldata[ldata.find(' is ')+4:].strip('?')
            self.query(q, nick, channel)




    def query(self, query, nick, channel):
        '''Querys the database for the factoid 'query', and returns its value to the channel if it is found'''
        if query in dict:
            self.msg(channel, str(dict[query].replace('%n', nick)))


    def add_factoid(self, query, nick):
        tmp = query
        try:
            if '<ACTION>'in query[1]:
                tmp[1] = str(tmp[1].replace('<ACTION>', '\x01ACTION ')+'\x01')
                dict[query[0]] = query[1]
            return True
        except IndexError:
            return False

    def query(self, query, nick, channel):
        '''Querys the database for the factoid 'query', and returns its value to the channel if it is found'''
        if query in dict:
                self.msg(channel, str(dict[query].replace('%n', nick)))

    def su_writedb(self, nick, channel, param = None):
        '''Writes the factoids database to the harddrive; Parameters: None'''
        write_dict()
        self.notice(channel, '<<Wrote Database>>')

    def su_add(self, nick, channel, param = None):
        '''Add a factoid; Parameters: a factoid name and a factoid body seperated by ":::" - For example, ?add test:::%n: it works!'''
        if param:
            query = param.split(':::', 1)
            if self.add_factoid(query, nick):
                self.notice(channel, '<<Added %s>>' % query)
            else:
                self.msg(channel, '%s: Adding of the factoid failed. Make sure you are using the proper syntax.' % nick)
        else:
            self.msg(channel,'%s: you must specify a factoid to add' % nick)

    def su_del(self, nick, channel, param = None):
        '''Delete a factoid; Parameters: factoid'''
        if param:
            del_factoid(param)
            self.notice(channel, '<<Deleting %s>>' % param)
        else:
            self.msg(channel, '%s: You must specify a factoid')
def write_dict():
    '''Write all factoids to the hard drive'''
    file = open(config.PATH + 'database.json', 'w')
    file.write(json.dumps(dict))
    file.close()
def del_factoid(query):
    '''Delete a factoid'''
    if query in dict:
        del dict[query]
def read_dict():
    '''Read factoids from the harddrive keep in RAM'''
    f = open('database.json')
    dict = json.load(f)
    f.close()
