import sqlite3

import api
import config


class Module(api.Module):
    def __init__(self, server):
        self.db = sqlite3.connect('wordstats.sqlite')
        self.c = self.db.cursor()
        self.c.execute('''create table if not exists stats (word text, spam, legit)''')
        self.db.commit()

        self.ratio = 0.01
        self.damp = 0.3

        self.kickat = 1.15
        self.spamat = 1.5
        self.legitat = 1
        self.banat = 1.5

        self.remove = ['-', '.', ', ', '_', '+', '\'', '"']
        api.module.__init__(self, server)

    def destroy(self):
        self.db.commit()
        del self.db, self.c

    def privmsg(self, nick, data, channel):
        pass

    def spam(self, data):
        for word in str(data).split():
            tmp = self.c.execute('''select * from stats where word = ?''', (self.safety(word),)).fetchall()
            if len(tmp) > 0:
                self.c.execute('''delete from stats where word = ?''', (self.safety(word),))
                self.c.execute('''insert into stats values (?, ?, ?)''', (self.safety(word), tmp[0][1] + 1, tmp[0][2]))
            else:
                self.c.execute('''insert into stats values (?, ?, ?)''', (self.safety(word), 2, 1))

    def legit(self, data):
        for word in data.split():
            tmp = self.c.execute('''select * from stats where word = ?''', (self.safety(word),)).fetchall()
            if len(tmp) > 0:
                self.c.execute('''delete from stats where word = ?''', (self.safety(word),))
                self.c.execute('''insert into stats values (?, ?, ?)''', (self.safety(word), tmp[0][1], tmp[0][2] + 1))
            else:
                self.c.execute('''insert into stats values (?, ?, ?)''', (self.safety(word), 1, 2))

    def zzz(self, data):
        for word in data.split():
            tmp = self.c.execute('''select * from stats where word = ?''', (self.safety(word),)).fetchall()
            self.msg('#bayesian', str(tmp))

    def check(self, data):
        self.msg('#bayesian', 'Level: %s' % self.get_stat(data))

    def get_stat(self, data):
        total = 0
        for word in data.split():
            tmp = self.c.execute('''select * from stats where word = ?''', (self.safety(word),)).fetchall()
            if len(tmp) > 0:
                total += ((float(tmp[0][1]) / float(tmp[0][2])) * self.ratio) / self.damp
        return total

    def safety(self, s):
        return str(s)
