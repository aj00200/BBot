from __future__ import division
import math

import api
import libs.mathwiz as geo

class Module(api.Module):
    def __init__(self, server):
        super(Module, self).__init__(server)
        api.hook_command('math', self.math, server)

    allow = {
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
    'geo.line(':'..22..', 
    'cm(':'..23..', 
    'in(':'..24..', 
    
    '!g':'6.67428', 
    '!pi':'3.1415926535897932384626433832795028841971693993751', 
    '!c':'299792458', 
    '!e':'2.7182818284590452353602874713526624977572', 
    '!F':'96485'
    }
    invert = {
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
    '..22..':'geo.line(', 
    '..23..':'geo.cm(', 
    '..24..':'geo.inch('
    }
    chars = '_ghijklmnopqrstuvwyz#@$\'"!:='

    def math(self, nick, channel, param = None):
        '''Functions and operators supported are: +, -, *, /, %, sqrt, pow, ceil, floor, log, sin, cos, tan'''
        if param:
            expr = param.lower()
            for each in self.allow:
                expr = expr.replace(each, ' %s ' % self.allow[each])
            for each in self.chars:
                expr = expr.replace(each, '')
            for each in self.invert:
                expr = expr.replace(' %s ' % each, self.invert[each])
            try:
                if '**' in expr:
                    raise Disallowed('**')
                self.msg(channel, str(eval(expr)))
            except Exception, e:
                self.report_error(channel, e)

    def report_error(self, channel, error):
        '''Report an error encountered while evaluating an expression
        to the channel from which the command orgionated'''
        self.msg(channel, 'Error %s; Arguments %s' % (type(error), error.args))

class Disallowed(Exception):
    def __init__(self, string):
        self.args = ['%s is not allowed!' % string]

class num(int):
    '''A class to hold a number in decimal, hex, and octal forms'''
    def __init__(self, number):
        self.hex = hex(number)
        self.dec = int(number)
        self.oct = oct(number)
        try:
            self.bin = bin(number)
        except Exception:
            self.bin = 'Upgrade to python2.6 or 2.7 please'

    def __str__(self):
        return '<hex %s; dec %s; oct %s; bin %s;>'% (self.hex, self.dec, self.oct, self.bin)

def hex2dec(hexnum):
    '''Convert a base 16 number to base 10'''
    return int(hexnum, 16)
def dec2hex(decimal):
    '''Convert a base 10 number to base 16'''
    return '%X' % decimal
def dec2oct(decimal):
    '''Convert a base 10 number to base 8'''
    return '%o' % decimal
def oct2dec(octal):
    '''Convert a base 8 number to base 10'''
    return int(oct(octal))
