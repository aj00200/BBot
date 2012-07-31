from __future__ import division
import math

def sort_dict(dict):
    '''Sort a dictionary'''
    items = dict.items()
    items.sort()
    return [value for key, value in items]

class Undefined(int):
    '''An undefined value that when combined with
    anything else will return undefined as well'''
    def __abs__(self):
        return self
    def __add__(self, y):
        return self
    def __and__(self, y):
        return False
    def __cmp__(self, y):
        return False
    def __div__(self, y):
        if isinstance(y, undefined):
            return 1
        else:
            return self
    def __divmod__(self, y):
        if isinstance(y, undefined):
            return 0
        else:
            return self
    def __float__(self):
        return self
    def __floordiv__(self, y):
        if isinstance(y, undefined):
            return 0
        else:
            return self
    def __index__(self, y):
        if isinstance(y, undefined):
            return 0
        else:
            return -1
    def __int__(self):
        return self
    def __invert__(self):
        return negative_undefined()
    def __long__(self):
        return self
    def __lshift__(self, y):
        return self
    def __mod__(self, y):
        if isinstance(y, undefined):
            return 0
        else:
            return self
    def __mul__(self, y):
        return self
    def __repr__(self):
        return '<undefined>'
    def __str__(self):
        return '<undefined>'

def midpoint(x, y, x2, y2):
    '''Calculate the midpoint between 2 points'''
    return '%s, %s' % ((x+x2)/2, (y+y2)/2)

def regular_polygn(sides, length = Undefined()):
    pass

def distance(x1, y1, x2, y2):
    '''Calculate the distance between 2 points'''
    return math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))

class Slope():
    def __init__(self, x1, y1, x2, y2):
        self.slope_rise = y2-y1
        self.slope_run = x2-x1
        if self.slope_rise<0 and self.slope_run<0:
            self.slope_rise = self.slope_rise*-1

            self.slope_run = self.slope_run*-1
    def __repr__(self):
        return '%s/%s' % (self.slope_rise, self.slope_run)

class Line():
    '''Class for creating line objects'''
    def __init__(self, x1, y1, x2, y2):
        self.points = ((x1, y1), (x2, y2))
        self.coords = Slope(x1, y1, x2, y2)

    def __repr__(self):
        return '<line slope = %s;>' % self.slope

    def points(self):
        return 'A: %s; B: %s' % (self.points[0], self.points[1])

class Polygon():
    '''Base class for all polygons'''
    def __init__(self):
        pass

    def points(self):
        sorted = sort_dict(self.coords)
        return 'A: %s; B: %s; C: %s;' % (sorted[0], sorted[1], sorted[2])

    def perimeter(self):
        '''Calculate the perimeter of the polygon'''
        p = 0.0
        for each in self.sides:
            p+= self.sides[each]
        return p

class Triangle(Polygon):
    '''Class for all triangle objects'''
    def __init__(self, axy, bxy, cxy):
        self.coords = {'A':axy, 'B':bxy, 'C':cxy}
        self.sides = {
            'ab':float(distance(axy[0], axy[1], bxy[0], bxy[1])), 
            'bc':float(distance(bxy[0], bxy[1], cxy[0], cxy[1])), 
            'ca':float(distance(cxy[0], cxy[1], axy[0], axy[1]))
        }
        self.centroid = '%s, %s' % (round((axy[0]+bxy[0]+cxy[0])/3.0, 4),
                                    round((axy[1]+bxy[1]+cxy[1])/3.0, 4))
        if self.sides['ab'] == self.sides['bc'] == self.sides['ca']:
            self.type = 'Equilateral'
        elif ((self.sides['ab'] == self.sides['bc']) 
              or (self.sides['ab'] == self.sides['ca']) 
              or (self.sides['bc'] == self.sides['ca'])):
            self.type = 'Isosceles'
        else:
            self.type = 'Scalene'

    def area(self):
        '''Return the area of the triangle'''
        return 0.5*(math.sqrt(math.pow(self.sides['ab'], 2) * 
                              math.pow(self.sides['ca'], 2) - 
                              math.pow(self.sides['ab'] * 
                                       self.sides['ca'], 2)))

    def __repr__(self):
        return '<triangle ab = %s; bc = %s; ca = %s; type = %s; centroid = (%s)>' % (
            self.sides['ab'], self.sides['bc'],
            self.sides['ca'], self.type, self.centroid)

class Quad(Polygon):
    '''Base class for all quadrilaterals'''
    pass

class Square(Quad):
    def __init__(self, ax, ay, bx, by, cx, cy, dx, dy):
        self.coords = {'A':(ax, ay), 'B':(bx, by), 'C':(cx, cy), 'D':(dx, dy)}
        self.sides = {'ab':float(distance(ax, ay, bx, by)), 
            'bc':float(distance(bx, by, cx, cy)), 
            'cd':float(distance(cx, cy, dx, dy)), 
            'da':float(distance(dx, dy, ax, ay))
        }

    def area(self):
        '''Return the area of the square'''
        return self.sides['ab']*self.sides['bc']

    def __repr__(self):
        return '<square ab = %s; bc = %s; cd = %s; da = %s;>' % (
            self.sides['ab'], self.sides['bc'],
            self.sides['cd'], self.sides['da'])

class Unit(float):
    '''Base class for all units'''
    pass

class Inch(Unit):
    '''Inches'''
    cm = 2.54
    ft = 1/12
    def __init__(self, num):
        self.num = num
    def __add__(self, y):
        if type(y) is inch:
            return inch(self.num+y)
        elif type(y) is cm:
            return inch(self.num+self.cm*y)
    def __mul__(self, y):
        if type(y) is inch:
            return inch(self.num*y)
        if type(y) is cm:
            return self.num*self.cm*y
    def __repr__(self):
        return '%sin' % self.num

class Cm(Unit):
    '''Centimeters'''
    inch = 0.393700787402
    def __init__(self, num):
        self.num = num
    def __mul__(self, y):
        if type(y) is cm:
            return cm(self.num*cm)
        elif type(y) is inch:
            return self.num*self.inch*y
    def __repr__(self):
        return '%scm' % self.num
