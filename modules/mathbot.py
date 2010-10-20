import q
import re
import api
import math
import config
import mathwiz as geo
class mathbot(api.module):
    commands=['math','math help','hex','dec2hex','dec2oct']
    def __init__(self,server=config.network):
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
            'tan(':'..12..',
            'geo.midpoint(':'..13..',
            'geo.triangle(':'..14..',
            'geo.distance(':'..15..',
            '.points(':'..16..',
            '.area(':'..17..',
            '.perimeter(':'..18..',
            'undefined':'..19..',
            'geo.square(':'..20..',
            'num(':'..21..',
            'geo.line(':'..22..'
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
            '..12..':'math.tan(',
            '..13..':'geo.midpoint(',
            '..14..':'geo.triangle(',
            '..15..':'geo.distance(',
            '..16..':'.points(',
            '..17..':'.area(',
            '..18..':'.perimeter(',
            '..19..':'geo.undefined()',
            '..20..':'geo.square(',
            '..21..':'num(',
            '..22..':'geo.line('
            }
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        self.ldata=data.lower()
        if ':'+config.cmd_char+'math help' in self.ldata:
            self.append((channel,nick+' : +, -, *, /, %, sqrt, pow, ceil, floor, log, asin, acos, atan, atan2, sin, cos, tan'))
        elif ':?math ' in self.ldata:
            self.e=data[data.find('?math ')+6:].strip('\r\n')
            self.e=self.e.replace('!pi','3.1415926535897931')
            self.e=self.e.replace('!e',str(math.e))
            for each in self.allow:
                self.e=self.e.replace(each,self.allow[each])
            self.chars='_ghijklmnopqrstuvwyz#@$\'\"!:=GHIJKLMNOPQRSTUVWYZ'
            for each in self.chars:
                self.e=self.e.replace(each,'')
            for each in self.invert:
                self.e=self.e.replace(each,self.invert[each])
            self.e=self.e.replace('//','.0/')
            try:
                if self.e.find('**')!=-1:
                    raise Disallowed('**')
                self.append((channel,str(eval(self.e))))
            except Exception,e:
                self.report_error(channel,e)
    def report_error(self,channel,e):
        self.append((channel,'Error %s; with arguments %s'%(type(e),e.args)))
class Disallowed(Exception):
    def __init__(self,string):
        self.args=['%s is not allowed!'%string]
#===Custom Functions===
class num(int):
    def __init__(self,num):
        self.hex=hex(num)
        self.dec=int(num)
        self.oct=oct(num)
        try:
            self.bin=bin(num)
        except:
            self.bin='Upgrade to python2.6 or 2.7 please'
    def __str__(self):
        return '<hex %s; dec %s; oct %s; bin %s;>'%(self.hex,self.dec,self.oct,self.bin)
def hex2dec(hex):
    return int(hex,16)
def dec2hex(dec):
    return '%X'%dec
def dec2oct(dec):
    return '%o'%dec
def oct2dec(oct):
    return int(oct(oct))
module=mathbot
