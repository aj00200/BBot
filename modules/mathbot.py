from __future__ import division
import q,re,api,math,config
import libs.mathwiz as geo
class module(api.module):
	commands=['math','math help','hex','dec2hex','dec2oct']
	allow={
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
	'!c':'2.99792458',
	'!e':'2.7182818284590452353602874713526624977572',
	'!F':'96485'
	}
	invert={
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
	chars='_ghijklmnopqrstuvwyz#@$\'"!:=GHIJKLMNOPQRSTUVWYZ'
	def privmsg(self,nick,data,channel):
		ldata=data.lower()
		if ':'+config.cmd_char+'math help' in ldata:
			self.msg(channel,nick+' : +, -, *, /, %, sqrt, pow, ceil, floor, log, asin, acos, atan, atan2, sin, cos, tan')
		elif ':%smath '%config.cmd_char in ldata:
			self.e=data[data.find('math ')+5:]
			for each in self.allow:
				self.e=self.e.replace(each,self.allow[each])
			for each in self.chars:
				self.e=self.e.replace(each,'')
			for each in self.invert:
				self.e=self.e.replace(each,self.invert[each])
			self.e=self.e.replace('//','.0/')
			try:
				if self.e.find('**')!=-1:
					raise Disallowed('**')
				self.msg(channel,str(eval(self.e)))
			except Exception,e:
				self.report_error(channel,e)
	def report_error(self,channel,e):
		self.msg(channel,'Error %s; with arguments %s'%(type(e),e.args))
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