import q
import re
import api
import math
import config
import mathwiz as geo
class mathbot(api.module):
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
            'geo.square(':'..20..'
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
            '..20..':'geo.square('
            }
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        self.ldata=data.lower()
        if ':?math help' in self.ldata:
            self.append((channel,nick+' : +, -, *, /, %, sqrt, pow, ceil, floor, log, asin, acos, atan, atan2, sin, cos, tan'))
        elif ':?math ' in self.ldata:
            self.e=self.ldata[self.ldata.find('?math ')+6:].strip('\r\n')
            self.e=self.e.replace('!pi','3.1415926535897931')
            self.e=self.e.replace('!e',str(math.e))
            for each in self.allow:
                self.e=self.e.replace(each,self.allow[each])
            self.chars='_abcdefghijklmnopqrstuvwxyz#@$\'\"!:='
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
                self.append((channel,self.e))
        elif ':?hex ' in self.ldata:
            try:
                self.e=self.ldata[self.ldata.find(':?hex ')+6:]
                self.append((channel,str(hex2dec(self.e))))
            except Exception,e:
                self.report_error(channel,e)
        elif ':?dec ' in self.ldata:
            try:
                self.e=int(self.ldata[self.ldata.find(':?dec ')+6:])
                self.append((channel,str(dec2hex(self.e))))
            except Exception,e:
                self.report_error(channel,e)
    def report_error(self,channel,e):
        self.append((channel,'Error %s; with arguments %s'%(type(e),e.args)))
class Disallowed(Exception):
    def __init__(self,string):
        self.args=['%s is not allowed!'%string]
#===Custom Functions===
def hex2dec(hex):
    return int(hex,16)
def dec2hex(dec):
    return '%X'%dec

module=mathbot
