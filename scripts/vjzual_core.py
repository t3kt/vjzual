__author__ = 'tekt'

def argToOp(arg):
	if not arg:
		return None
	if isinstance(arg, str):
		o = op(arg)
		if not o:
			raise Exception('operator not found: ' + arg)
		return o
	return arg

def argToPath(arg):
	if not arg:
		return ''
	if isinstance(arg, str):
		return arg
	if hasattr(arg, 'path'):
		return arg.path
	return arg

def toggleCooking(path, delayFrames=1):
	path = argToPath(path)
	op(path).allowCooking = False
	run('op("' + path + '").allowCooking = True', delayFrames=delayFrames)

def toggleExport(path, delayFrames=1):
	path = argToPath(path)
	op(path).export = False
	run('op("' + path + '").export = True', delayFrames=delayFrames)

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
	tbl = argToOp(tbl)
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

def overrideRows(tbl, overrides):
	tbl = argToOp(tbl)
	if not tbl:
		return
	for key in overrides:
		tbl[key, 1] = overrides[key]

class VjzParam:
	def __init__(self, comp):
		self._comp = comp

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

	def saveParamValue(self, tbl):
		val = self.paramValue
		updateTableRow(tbl, self.paramName, {'value': val}, addMissing=True)

class VjzModule:
	def __init__(self, comp):
		self._comp = comp

	def mVar(self, name):
		return self._comp.var(name)

	@property
	def modName(self):
		return self.mVar('modname')

	@property
	def modParamNames(self):
		ptbl = VJZ.paramTable
		mname = self.modName
		pnames = []
		for p in ptbl.col('name')[1:]:
			if ptbl[p, 'module'] == mname:
				print('param "' + p + '" DOES belong to module "' + mname + '"')
				pnames.append(p.val)
			else:
				print('param "' + p + '" does NOT belong to module "' + mname + '"')
		return pnames

	@property
	def modParamObjects(self):
		pnames = self.modParamNames
		for p in pnames:
			pop = self._comp.op(p + '_param')
			if not pop:
				print('parameter component not found for param "' + p + '" in module "' + self.modName + '"')
			yield pop

class VjzSystem:
	def __init__(self, root):
		self._root = root

	def sVar(self, name):
		return self._root.var(name)

	def op(self, path):
		return self._root.op(path)

	@property
	def moduleTable(self):
		return self._root.op(self.sVar('moduletbl'))

	@property
	def paramTable(self):
		return self._root.op(self.sVar('paramtbl'))

	def getModules(self, fakes=False):
		modtbl = self.moduleTable
		for mname in modtbl.col('name')[1:]:
			if not fakes and modtbl[mname, 'fake'] == '1':
				continue
			mop = self._root.op(modtbl[mname, 'path'])
			if mop:
				yield mop

	def getModule(self, name):
		m = self.moduleTable[name, 'path']
		m = op(m) if m else None
		if m is None:
			raise Exception('module not found: "' + name + '"')
		return m

VJZ = VjzSystem(op('/_'))