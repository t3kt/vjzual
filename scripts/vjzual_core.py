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

def toggleBypass(path, delayFrames=1):
	path = argToPath(path)
	op(path).bypass = True
	run('op("' + path + '").bypass = False', delayFrames=delayFrames)

def nameToAbbr(name):
	if ':' in name:
		dev, ctl = name.split(':')
		return dev[0] + ':' + ctl
	return name

def _midiAbbrToName(comp, abbr):
	ctrlmap = comp.op(comp.var('midictrlabbrmap'))
	n = ctrlmap[abbr, 'name']
	return n.val if n else None

def updateTableRow(tbl, rowKey, vals, addMissing=False, ignoreMissingCols=False):
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
		if ignoreMissingCols and tbl[rowKey, colKey] is None:
			continue
		tbl[rowKey, colKey] = v if v is not None else ''

def overrideRows(tbl, overrides):
	tbl = argToOp(tbl)
	if not tbl:
		return
	for key in overrides:
		tbl[key, 1] = overrides[key]

def prepFilterList(filterstr):
	if isinstance(filterstr, Cell):
		filterstr = filterstr.val
	if not filterstr:
		return None
	if '|' in filterstr:
		return filterstr.split('|')
	return [filterstr]

def rowsToDictList(tbl):
	tbl = argToOp(tbl)
	if not tbl:
		return []
	allObjs = []
	cols = [c.val for c in tbl.row(0)]
	for i in range(1, tbl.numRows):
		obj = {c: tbl[i, c].val for c in cols}
		allObjs.append(obj)
	return allObjs

def buildModuleDefDicts(moduletbl, paramtbl):
	moduletbl, paramtbl = argToOp(moduletbl), argToOp(paramtbl)
	mDicts = rowsToDictList(moduletbl)
	if not mDicts:
		return None
	mDicts = [withoutDictEmptyStrings(m) for m in mDicts]
	pDicts = rowsToDictList(paramtbl)
	pDicts = [withoutDictEmptyStrings(p) for p in pDicts]
	for p in pDicts:
		modname = p['module']
		if modname:
			for m in mDicts:
				if m['name'] == modname:
					if not 'paramdefs' in m:
						m['paramdefs'] = []
					m['paramdefs'].append(p)
					break
	return mDicts

def extractModuleTblFromDicts(moduleDicts, moduletbl):
	moduletbl = argToOp(moduletbl)
	moduletbl.setSize(1, moduletbl.numCols)
	for mDict in moduleDicts:
		updateTableRow(moduletbl, mDict['name'], mDict, addMissing=True, ignoreMissingCols=True)

def extractParamTableFromDicts(moduleDicts, paramtbl):
	paramtbl = argToOp(paramtbl)
	paramtbl.setSize(1, paramtbl.numCols)
	for mDict in moduleDicts:
		if not 'paramdefs' in mDict:
			continue
		for pDict in mDict['paramdefs']:
			updateTableRow(paramtbl, pDict['name'], pDict, addMissing=True, ignoreMissingCols=True)

def withoutDictEmptyStrings(d):
	return {k: d[k] for k in d if d[k] != ""}

def DEBUGLOG(s):
	log = op('/_/LOG')
	log.text += s + '\n'
	log.save('DEBUGLOG.txt')
	pass

def getOrAddParamPage(comp, name):
	comp = argToOp(comp)
	for page in comp.customPages:
		if page.name == name:
			return page
	return comp.appendCustomPage(name)

def _logDeprecatedCall(self, methodName):
	if hasattr(self, '_comp') and self._comp:
		selfName = self._comp.path
	else:
		selfName = str(self)
	print('deprecated extension method "' + methodName + '" called on [' + type(self).__name__ + '] ' + selfName)

def deprecatedMethod(origFn):
	def newFn(*args, **kwargs):
		_logDeprecatedCall(args[0], origFn.__name__)
		return origFn(*args, **kwargs)
	return newFn

class VjzParam:
	def __init__(self, comp):
		self._comp = comp

	@staticmethod
	def get(comp):
		if hasattr(comp, 'paramDef'):
			return comp
		if comp.ext and hasattr(comp.ext, 'VjzParam'):
			return comp.ext.VjzParam
		if comp.extensions:
			for e in comp.extensions:
				if isinstance(e, VjzParam):
					return e
		print('unable to find VjzParam extension for comp: ' + comp.path)
		return None

	@deprecatedMethod
	def pVar(self, name):
		return self.PVar(name)

	@deprecatedMethod
	@property
	def paramDef(self):
		return self.ParamDef

	@property
	@deprecatedMethod
	def paramValue(self):
		return self.ParamValue

	@paramValue.setter
	@deprecatedMethod
	def paramValue(self, val):
		self.ParamValue = val

	@property
	@deprecatedMethod
	def paramName(self):
		return self.ParamName

	@property
	@deprecatedMethod
	def paramMidiMapping(self):
		return self.ParamMidiMapping

	@property
	@deprecatedMethod
	def paramMidiName(self):
		return self.ParamMidiName

	@paramMidiName.setter
	@deprecatedMethod
	def paramMidiName(self, name):
		self.ParamMidiName = name

	@deprecatedMethod
	def updateParamTableEntry(self, vals):
		self.UpdateParamTableEntry(vals)

	@deprecatedMethod
	def saveParamMidiMapping(self):
		return self.SaveParamMidiMapping()

	@deprecatedMethod
	def loadParamMidiMapping(self):
		return self.LoadParamMidiMapping()

	@deprecatedMethod
	def saveParamValue(self, tbl):
		self.SaveParamValue(tbl)

	@deprecatedMethod
	def loadParamValue(self, tbl):
		self.LoadParamValue(tbl)

	@deprecatedMethod
	def resetParamToDefault(self):
		return self.ResetParamToDefault()

	def PVar(self, name):
		return self._comp.var(name)

	@property
	def ParamDef(self):
		d = self._comp.op(self.PVar('pdef'))
		return d if d.numRows == 2 else None

	@property
	def ParamValue(self):
		return self._comp.op('value')[0][0]

	@ParamValue.setter
	def ParamValue(self, val):
		self._comp.op('slider').panel.u = val

	@property
	def ParamName(self):
		return self.PVar('pname')

	@property
	def ParamMidiMapping(self):
		mapping = self._comp.op('mapping')
		return mapping if mapping.numRows == 2 else None

	@property
	def ParamMidiName(self):
		m = self.paramMidiMapping
		return m[1, 'name'].val if m else None

	@ParamMidiName.setter
	def ParamMidiName(self, name):
		if not name or name == '-':
			abbr = '-'
			i = 0
		else:
			ctrlmap = self._comp.op(self.PVar('midictrlabbrmap'))
			abbr = nameToAbbr(name)
			n = ctrlmap[abbr, 'abbr']
			if n:
				i = n.row + 1
			else:
				abbr = '-'
				i = 0
		self._comp.op('midictllist/set').run(i, abbr)

	def UpdateParamTableEntry(self, vals):
		updateTableRow(self.PVar('editableparamtbl'), self.paramName, vals)

	def SaveParamMidiMapping(self):
		mapping = self.paramMidiMapping
		if not mapping:
			dev, ctl = '', ''
		else:
			dev, ctl = mapping[1, 'mididev'].val, mapping[1, 'midictl'].val
		self.updateParamTableEntry({'mididev': dev, 'midictl': ctl})

	def LoadParamMidiMapping(self):
		pdef = self.paramDef
		if not pdef:
			return
		dev, ctl = pdef[1, 'mididev'].val, pdef[1, 'midictl'].val
		if not dev or not ctl:
			self.paramMidiName = None
		else:
			self.paramMidiName = dev[0] + ':' + ctl

	def SaveParamValue(self, tbl):
		val = self.paramValue
		updateTableRow(tbl, self.paramName, {'value': val}, addMissing=True)

	def LoadParamValue(self, tbl):
		val = tbl[self.paramName, 1]
		if val is not None:
			self.paramValue = float(val)

	def ResetParamToDefault(self):
		val = self.paramDef[1, 'default']
		if val is None:
			raise Exception('Parameter {0} does not have a default value and cannot be reset'.format(self.paramName))
		self.paramValue = val.val

class VjzModule:
	def __init__(self, comp):
		self._comp = comp

	@staticmethod
	def get(comp):
		if hasattr(comp, 'modName'):
			return comp
		if comp.ext and hasattr(comp.ext, 'VjzModule'):
			return comp.ext.VjzModule
		if comp.extensions:
			for e in comp.extensions:
				if isinstance(e, VjzModule):
					return e
		print('unable to find VjzModule extension for comp: ' + comp.path)
		return None

	@deprecatedMethod
	def mVar(self, name):
		return self.MVar(name)

	@property
	@deprecatedMethod
	def modName(self):
		return self.ModName

	@property
	@deprecatedMethod
	def modPath(self):
		return self.ModPath

	@property
	@deprecatedMethod
	def modParamTable(self):
		return self.ModParamTable

	@property
	@deprecatedMethod
	def modParamNames(self):
		return self.ModParamNames

	@property
	@deprecatedMethod
	def modParamLocalNames(self):
		return self.ModParamLocalNames

	@property
	@deprecatedMethod
	def modParamObjects(self):
		return self.ModParamObjects

	@deprecatedMethod
	def modParam(self, name):
		return self.ModParam(name)

	@deprecatedMethod
	def saveParamValues(self, tbl):
		return self.SaveParamValues(tbl)

	@deprecatedMethod
	def loadParamValues(self, tbl):
		return self.LoadParamValues(tbl)

	@deprecatedMethod
	def resetParamsToDefaults(self):
		return self.ResetParamsToDefaults()

	def MVar(self, name):
		return self._comp.var(name)

	@property
	def ModName(self):
		return self.mVar('modname')

	@property
	def ModPath(self):
		return self._comp.path

	@property
	def ModParamTable(self):
		return self._comp.op(self.mVar('modparamtbl'))

	@property
	def ModParamNames(self):
		return [c.val for c in self.modParamTable.col('name')[1:]]

	@property
	def ModParamLocalNames(self):
		return [c.val for c in self.modParamTable.col('localname')[1:]]

	@property
	def ModParamObjects(self):
		pnames = self.modParamLocalNames
		for p in pnames:
			pop = self.modParam(p)
			if not pop:
				print('parameter component not found for param "' + p + '" in module "' + self.modName + '"')
			yield pop

	def ModParam(self, name):
		pop = self._comp.op(name + '_param')
		return VjzParam.get(pop) if pop else None

	def SaveParamValues(self, tbl):
		tbl = argToOp(tbl)
		print('saving module ' + self.modName + ' to ' + tbl.path)
		pnames = self.modParamLocalNames
		pvals = self._comp.op(self.mVar('modparamsout'))
		for p in pnames:
			pop = self.modParam(p)
			if pop:
				pop.saveParamValue(tbl)
				continue
			elif pvals:
				c = pvals.chan(p)
				if c is not None:
					updateTableRow(tbl, p, {'value': c[0]})
					continue
			print('cannot save parameter ' + p)

	def LoadParamValues(self, tbl):
		tbl = argToOp(tbl)
		pnames = self.modParamLocalNames
		for p in pnames:
			pop = self.modParam(p)
			if pop:
				pop.loadParamValue(tbl)
			else:
				print('cannot load parameter ' + self.modPath + ' : ' + p)

	def ResetParamsToDefaults(self):
		for p in self.modParamObjects:
			p.resetParamToDefault()

class VjzSystem:
	def __init__(self, root):
		self._root = root

	@deprecatedMethod
	def sVar(self, name):
		return self.SVar(name)

	@property
	@deprecatedMethod
	def moduleTable(self):
		return self.ModuleTable

	@property
	@deprecatedMethod
	def paramTable(self):
		return self.ParamTable

	@deprecatedMethod
	def getModules(self, fakes=False):
		return self.GetModules(fakes=fakes)

	@deprecatedMethod
	def getModule(self, name):
		return self.GetModule(name)

	@deprecatedMethod
	def saveParamValues(self):
		return self.SaveParamValues()

	@deprecatedMethod
	def loadParamValues(self):
		return self.LoadParamValues()

	def SVar(self, name):
		return self._root.var(name)

	@property
	def ModuleTable(self):
		return self._root.op(self.sVar('moduletbl'))

	@property
	def ParamTable(self):
		return self._root.op(self.sVar('paramtbl'))

	def GetModules(self, fakes=False):
		modtbl = self.moduleTable
		for mname in modtbl.col('name')[1:]:
			if not fakes and modtbl[mname, 'fake'] == '1':
				continue
			mop = self._root.op(modtbl[mname, 'path'])
			if mop:
				m = VjzModule.get(mop)
				if m:
					yield m

	def GetModule(self, name):
		m = self.moduleTable[name, 'path']
		m = op(m) if m else None
		if m is None:
			raise Exception('module not found: "' + name + '"')
		return VjzModule.get(m)

	def SaveParamValues(self):
		tbl = self._root.op(self.sVar('paramstatetbl'))
		for m in self.getModules():
			m.saveParamValues(tbl)
		tbl.save(tbl.par.file.val)

	def LoadParamValues(self):
		tbl = self._root.op(self.sVar('paramstatetbl'))
		for m in self.getModules():
			print('loading param values in: ', m.modPath)
			m.loadParamValues(tbl)

VJZ = VjzSystem(op('/_'))