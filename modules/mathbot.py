import q
import math
class mathbot():
    def __init__(self):

        self.allow={
            ')':'..0..',
            'sqrt(':'..1..',
            'pow(':'..2..',
            'ceil(':'..3..',
            'floor(':'..4..',
            'log(':'..5..',
            'asin(':'..6..',
            'acos(':'..7..',
            'atan(':'..8..',
            'atan2(':'..9..',
            'sin(':'..10..',
            'cos(':'..11..',
            'tan(':'..12..'
            }
        self.invert={
            '..0..':')',
            '..1..':'math.sqrt(',
            '..2..':'math.pow(',
            '..3..':'math.ceil(',
            '..4..':'math.floor(',
            '..5..':'math.log(',
            '..6..':'math.asin(',
            '..7..':'math.acos(',
            '..8..':'math.atan(',
            '..9..':'math.atan2(',
            '..10..':'math.sin(',
            '..11..':'math.cos(',
            '..12..':'math.tan('
            }
    def go(self,nick,data,channel):
        self.ldata=data.lower()
        if self.ldata.find(':?math help')!=-1:
            q.queue.append((channel,nick+' : +, -, *, /, %, sqrt, pow, ceil, floor, log, asin, acos, atan, atan2, sin, cos, tan'))
        elif self.ldata.find(':?math ')!=-1:
            if self.ldata.find('**')!=-1:
                q.queue.append((channel,'Please use pow instead of **'))
                self.ldata='?math 0'
            self.e=self.ldata[self.ldata.find('?math ')+6:].strip('\r\n')
            self.e=self.e.replace('!pi','3.1415926535897931')
            self.e=self.e.replace('!e',str(math.e))
            for each in self.allow:
                self.e=self.e.replace(each,self.allow[each])
            self.chars='_abcdefghijklmnopqrstuvwxyz#@$\'\"()!:='
            for each in self.chars:
                self.e=self.e.replace(each,'')
            for each in self.invert:
                self.e=self.e.replace(each,self.invert[each])
            self.e=self.e.replace('//','.0/')
            try:
                q.queue.append((channel,str(eval(self.e))))
            except Exception,e:
                self.e='Error: %s; with arguments %s'%(type(e),e.args)
                q.queue.append((channel,self.e))
