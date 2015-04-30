__author__ = 'tekt'

def nameToAbbr(name):
	if ':' in name:
		dev, ctl = name.split(':')
		return dev[0] + ':' + ctl
	return name

def _midiAbbrToName(comp, abbr):
	ctrlmap = comp.op(comp.var('midictrlabbrmap'))
	n = ctrlmap[abbr, 'name']
	return n.val if n else None

def updateTableRow(tbl, rowKey, vals, addMissing=False):
	if isinstance(tbl, str):
		t = op(tbl)
		if not t:
			raise Exception('table not found: ' + tbl)
		tbl = t
	if not tbl:
		return
	if not tbl[rowKey, 0]:
		if not addMissing:
			raise Exception('row ' + rowKey + ' not found in table ' + tbl)
		else:
			tbl.appendRow([rowKey])
	for colKey in vals:
		v = vals[colKey]
		tbl[rowKey, colKey] = v if v is not None else ''

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
		d = self._comp.op(self.pVar('pdef'))
		return d if d.numRows == 2 else None

	@property
	def paramValue(self):
		return self._comp.op('value')[0][0]

	@paramValue.setter
	def paramValue(self, val):
		self._comp.op('slider').panel.u = val

	@property
	def paramName(self):
		return self.pVar('pname')

	@property
	def paramMidiMapping(self):
		mapping = self._comp.op('mapping')
		return mapping if mapping.numRows == 2 else None

	@property
	def paramMidiName(self):
		m = self.paramMidiMapping
		return m[1, 'name'].val if m else None

	@paramMidiName.setter
	def paramMidiName(self, name):
		if not name or name == '-':
			abbr = '-'
			i = 0
		else:
			ctrlmap = self._comp.op(self.pVar('midictrlabbrmap'))
			abbr = nameToAbbr(name)
			n = ctrlmap[abbr, 'abbr']
			if n:
				i = n.row + 1
			else:
				abbr = '-'
				i = 0
		self._comp.op('midictllist/set').run(i, abbr)

	def updateParamTableEntry(self, vals):
		updateTableRow(self.pVar('editableparamtbl'), self.paramName, vals)

	def saveParamMidiMapping(self):
		mapping = self.paramMidiMapping
		if not mapping:
			dev, ctl = '', ''
		else:
			dev, ctl = mapping[1, 'mididev'].val, mapping[1, 'midictl'].val
		self.updateParamTableEntry({'mididev': dev, 'midictl': ctl})

	def loadParamMidiMapping(self):
		pdef = self.paramDef
		if not pdef:
			return
		dev, ctl = pdef[1, 'mididev'].val, pdef[1, 'midictl'].val
		if not dev or not ctl:
			self.paramMidiName = None
		else:
			self.paramMidiName = dev[0] + ':' + ctl

class VjzModule:
	pass
