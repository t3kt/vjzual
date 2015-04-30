__author__ = 'tekt'

class VjzParam:
	def __init__(self, comp):
		self._comp = comp

	def sayHi(self):
		print('hi! self: ', self)
		print('hi! self.comp: ', self._comp)

	def initParam(self):
		print('initializing parameter ', self._comp.path)
		self._comp.op('init').module.init()

	def pVar(self, name):
		return self._comp.var(name)

	@property
	def paramDef(self):
		return self._comp.op(self.pVar('pdef'))

	@property
	def paramValue(self):
		return self._comp.op('value')[0][0]

	@paramValue.setter
	def paramValue(self, val):
		self._comp.op('slider').panel.u = val

class VjzModule:
	pass
