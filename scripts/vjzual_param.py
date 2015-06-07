__author__ = 'tekt'

try:
	import vjzual_core as vjzual
except ImportError:
	vjzual = mod.vjzual

class VjzualParam:
	def __init__(self, comp):
		self.comp = comp
		self.initParameters()

	def initParameters(self):
		page = vjzual.getOrAddParamPage(self.comp, 'vjzparam')
		page.appendStr('Pname', label='parameter name')
		pass
