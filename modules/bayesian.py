import q,api,config,sqlite3
class module(api.module):
    def __init__(self,server):
        self.db=sqlite3.connect('wordstats.sqlite')
        self.c=self.db.cursor()
        self.c.execute('''create table if not exists stats (word text, spam, legit)''')
        self.db.commit()
        
        self.ratio=0.01
        self.damp=0.3
        
        self.kickat=3
        self.spamat=4
        self.legitat=0.8
        self.banat=100
        
        self.remove=['-','.',',','_','+','\'','"']
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        data=data.lower()
        for each in self.remove:
            data=data.replace(each,'')
            stat=self.get_stat(api.getMessage(data))
        if api.checkIfSuperUser(data):
            if '?spam ' in data:
                self.spam(data[data.find('spam ')+5:].lower())
                return
            elif '?legit ' in data:
                self.legit(data[data.find('legit ')+6:].lower())
                return
            elif '?check ' in data:
                self.check(data[data.find('check ')+6:].lower())
                return
            elif '?zzz ' in data:
                self.zzz(data[data.find('zzz ')+4:].lower())
                return
            elif '?comba' in data:
                self.db.commit()
                return
        else:
            if stat>self.kickat:
                self.kick(nick,channel,'%s'%stat)
        if stat>self.spamat:
            self.spam(api.getMessage(data))
        elif stat<self.legitat:
            self.legit(api.getMessage(data))
    def spam(self,data):
        for word in data.split():
            tmp=self.c.execute('''select * from stats where word=?''',(word,)).fetchall()
            if len(tmp)>0:
                self.c.execute('''delete from stats where word=?''',(word,))
                self.c.execute('''insert into stats values (?, ?, ?)''',(word,tmp[0][1]+1,tmp[0][2]))
            else:
                self.c.execute('''insert into stats values (?, ?, ?)''',(word,2,1))
    def legit(self,data):
        for word in data.split():
            tmp=self.c.execute('''select * from stats where word=?''',(word,)).fetchall()
            if len(tmp)>0:
                self.c.execute('''delete from stats where word=?''',(word,))
                self.c.execute('''insert into stats values (?, ?, ?)''',(word,tmp[0][1],tmp[0][2]+1))
            else:
                self.c.execute('''insert into stats values (?, ?, ?)''',(word,1,2))
    def zzz(self,data):
        for word in data.split():
            tmp=self.c.execute('''select * from stats where word=?''',(word,)).fetchall()
            self.append(('#bayesian',str(tmp)))
    def check(self,data):
        self.append(('#bayesian','Level: %s'%self.get_stat(data)))
    def get_stat(self,data):
        total=0
        for word in data.split():
            tmp=self.c.execute('''select * from stats where word=?''',(word,)).fetchall()
            if len(tmp)>0:
                total+=((float(tmp[0][1])/float(tmp[0][2]))*self.ratio)/self.damp
        return total