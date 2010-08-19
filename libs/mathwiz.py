import math
def sort_dict(dict):
    items = dict.items()
    items.sort()
    return [value for key, value in items]
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
        return self
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
    def __repr__(self):
        return '<undefined>'
    def __str__(self):
        return '<undefined>'

def midpoint(x,y,x2,y2):
    return '%s,%s'%((x+x2)/2,(y+y2)/2)
def regular_polygn(sides,length=undefined()):
    pass
def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
class polygon():
    def __init__(self):
        pass
    def points(self):
        sorted=sort_dict(self.coords)
        return 'A: %s; B: %s; C: %s;'%(sorted[0],sorted[1],sorted[2])
    def perimeter(self):
        p=0.0
        for each in self.sides:
            p+=self.sides[each]
        return p
class triangle(polygon):
    def __init__(self,ax,ay,bx,by,cx,cy):
        self.coords={'A':(ax,ay),'B':(bx,by),'C':(cx,cy)}
        self.sides={'ab':float(distance(ax,ay,bx,by)),
            'bc':float(distance(bx,by,cx,cy)),
            'ca':float(distance(cx,cy,ax,ay))
        }
        self.centroid='%s,%s'%(round((ax+bx+cx)/3.0,4),round((ay+by+cy)/3.0,4))
        if self.sides['ab']==self.sides['bc']==self.sides['ca']:
            self.type='Equilateral'
        elif (self.sides['ab']==self.sides['bc']) or (self.sides['ab']==self.sides['ca']) or (self.sides['bc']==self.sides['ca']):
            self.type='Isosceles'
        else:
            self.type='Scalene'
    def area(self):
        return 0.5*(math.sqrt(math.pow(self.sides['ab'],2)*math.pow(self.sides['ca'],2)-math.pow(self.sides['ab']*self.sides['ca'],2)))
    def __repr__(self):
        return '<triangle ab=%s; bc=%s; ca=%s; type=%s; centroid=(%s)>'%(self.sides['ab'],self.sides['bc'],self.sides['ca'],self.type,self.centroid)
class quad(polygon):
    pass
class square(polygon,quad):
    def __init__(self,ax,ay,bx,by,cx,cy,dx,dy):
        self.coords={'A':(ax,ay),'B':(bx,by),'C':(cx,cy),'D':(dx,dy)}
        self.sides={'ab':float(distance(ax,ay,bx,by)),
            'bc':float(distance(bx,by,cx,cy)),
            'cd':float(distance(cx,cy,dx,dy)),
            'da':float(distance(dx,dy,ax,ay))
        }
    def area(self):
        return self.sides['ab']*self.sides['bc']
    def __repr__(self):
        return '<square ab=%s; bc=%s; cd=%s; da=%s;>'%(self.sides['ab'],self.sides['bc'],self.sides['cd'],self.sides['da'])