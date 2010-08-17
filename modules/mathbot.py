import q
import api
import math
import config
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
            'geo.distance(':'..15..'
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
            '..15..':'geo.distance('
            }
        api.module.__init__(self,server)
    def go(self,nick,data,channel):
        self.ldata=data.lower()
        if self.ldata.find(':?math help')!=-1:
            self.append((channel,nick+' : +, -, *, /, %, sqrt, pow, ceil, floor, log, asin, acos, atan, atan2, sin, cos, tan'))
        elif self.ldata.find(':?math ')!=-1:
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
        elif self.ldata.find(':?hex ')!=-1:
            try:
                self.e=self.ldata[self.ldata.find(':?hex ')+6:]
                self.append((channel,str(hex2dec(self.e))))
            except Exception,e:
                self.report_error(channel,e)
        elif self.ldata.find(':?dec ')!=-1:
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
class undefined(int):
    def __abs__(self):
        return self
    def __add__(self,y):
        return self
    def __and__(self,y):
        return False
    def __cmp__(self,y):
        return False
    def __div__(self,y):
        if isinstance(y,undefined):
            return 1
        else:
            return self
    def __divmod__(self,y):
        if isinstance(y,undefined):
            return 0
        else:
            return self
    def __float__(self):
        return self
    def __floordiv__(self,y):
        if isinstance(y,undefined):
            return 0
        else:
            return self
    def __index__(self,y):
        if isinstance(y,undefined):
            return 0
        else:
            return -1
    def __int__(self):
        return 0
    def __invert__(self):
        return negative_undefined()
    def __long__(self):
        return self
    def __lshift__(self,y):
        return self
    def __mod__(self,y):
        if isinstance(y,undefined):
            return 0
        else:
            return self
    def __mul__(self,y):
        return self

class geomath():
    def midpoint(self,x,y,x2,y2):
        return '%s,%s'%((x+x2)/2,(y+y2)/2)
    def triangle(self,ax,ay,bx,by,cx,cy):
        ab=float(self.distance(ax,ay,bx,by))
        bc=float(self.distance(bx,by,cx,cy))
        ca=float(self.distance(cx,cy,ax,ay))
        centroid='%s,%s'%(round((ax+bx+cx)/3.0,4),round((ay+by+cy)/3.0,4))
        if ab==bc==ca:
            type='Equilateral'
        elif (ab==bc) or (ab==ca) or (bc==ca):
            type='Isosceles'
        else:
            type='Scalene'
        return '<triangle ab=%s; bc=%s; ca=%s; type=%s; centroid=(%s)>'%(ab,bc,ca,type,centroid)
    def regular_polygn(self,sides,length=undefined()):
        pass
    def distance(self,x1,y1,x2,y2):
        return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
        
geo=geomath()
module=mathbot
