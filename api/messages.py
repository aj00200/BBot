class IRCEvent():
    def __init__(self, connection, raw):
        self.connection = connection
        self.raw = raw

class UserEvent(IRCEvent):
    def __init__(self, connection, raw):
        self.nick = raw[1:raw.index('!')]
        self.ident = raw[raw.index('!')+1:raw.index('@')]
        self.host = raw[raw.index('@')+1:raw.index(' ')]

class Message(UserEvent):
    def __init__(self, connection, raw):
        self.text = raw[raw.index(' :')+2:]

    def reply(self, message):
        pass

class Privmsg(Message):
    def __init__(self, connection, raw):
        super(Privmsg, self).__init__(connection, raw)
        self.target = raw[raw.index(' PRIVMSG ')+9:raw.index(' :')]
        if self.target == self.connection.nick: # Personal message
            self.personal = True
            self.channel = None
        else:
            self.personal = False
            self.channel = self.target

    def reply(self, message):
        if self.personal:
            reply_to = self.nick
        elif self.channel:
            reply_to = self.channel

        connection.push('PRIVMSG %s :%s' % (reply_to, message))

class Notice(Message):
    def __init__(self, connection, raw):
        super(Notice, self).__init__(connection, raw)
        self.channel = raw[raw.index(' NOTICE ')+8:raw.index(' :')]

    def reply(self, message):
        if self.channel == self.connection.nick:
            reply_to = self.nick # Message is a pm
        else:
            reply_to = self.channel
        self.connection.push('NOTICE %s :%s' % (reply_to, message))

class Join(UserEvent):
    def __init__(self, connection, raw):
        super(Join, self).__init__(connection, raw)
        self.channel = raw[raw.index(' :')+2:]

class Mode(UserEvent):
    def __init__(self, connection, raw):
        super(Mode, self).__init__(connection, raw)
        _, __, self.channel, self.mode = raw.split()

class Code(IRCEvent):
    def __init__(self, connection, raw):
        super(Code, self).__init__(connection, raw)
        _, code, self.nick, self.message = raw.split(' ', 3)
        self.code = int(code)
