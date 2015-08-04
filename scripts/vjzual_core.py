from abc import abstractproperty, ABCMeta, abstractmethod

__author__ = 'tekt'

import json

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
		obj = {c: tbl[i, c].val for c in cols if tbl[i, c] != ""}
		allObjs.append(obj)
	return allObjs

def fillTableFromDicts(tbl, objs, cols=None, keyCol='name'):
	tbl = argToOp(tbl)
	tbl.clear()
	tbl.appendRow(cols)
	if not len(objs):
		return
	for obj in objs:
		if not len(obj):
			continue
		updateTableRow(tbl, obj[keyCol], withoutDictEmptyStrings(obj), addMissing=True, ignoreMissingCols=False)

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

def _safeTestForAttr(comp, name):
	# This throws a 'object has no attribute..' exception even though it's
	# just a hasattr() check, probably due to TD's promoted extension lookup
	try:
		return hasattr(comp, name)
	except:
		return False

def toggleTag(comp, name, enable):
	comp = argToOp(comp)
	if enable:
		comp.tags.add(name)
	elif name in comp.tags:
		comp.tags.remove(name)

def notImplemented(*unused_args):
	raise NotImplementedError()

def make_getterNotImplemented():
	return lambda self: notImplemented()

def make_setterNotImplemented():
	return lambda self, value: notImplemented()

def _override(func):
	return func

class VjzParamBase:
	__metaclass__ = ABCMeta

	@abstractmethod
	def PVar(self, name):
		notImplemented(self, name)

	@abstractmethod
	def GetParamDefProperty(self, name):
		notImplemented(name)

	ParamValue_getter = make_getterNotImplemented()
	ParamValue_setter = make_setterNotImplemented()
	ParamValue = abstractproperty(ParamValue_getter, ParamValue_setter)

	@property
	def ParamName(self):
		return self.PVar('pname')

	ParamMidiName_getter = make_getterNotImplemented()
	ParamMidiName_setter = make_setterNotImplemented()
	ParamMidiName = abstractproperty(ParamMidiName_getter, ParamMidiName_setter)

	@abstractmethod
	def UpdateParamTableEntry(self, vals):
		notImplemented(self, vals)

	def SaveParamMidiMapping(self):
		notImplemented(self)

	def LoadParamMidiMapping(self):
		dev, ctl = self.GetParamDefProperty('mididev'), self.GetParamDefProperty('midictl')
		if not dev or not ctl:
			self.ParamMidiName = None
		else:
			self.ParamMidiName = dev[0] + ':' + ctl

	def ResetParamToDefault(self):
		val = self.GetParamDefProperty('default')
		if val is None:
			raise Exception('Parameter {0} does not have a default value and cannot be reset'.format(self.ParamName))
		self.ParamValue = val.val

	def SaveParamValue(self, tbl):
		val = round(self.ParamValue, 4)
		updateTableRow(tbl, self.ParamName, {'value': val}, addMissing=True)

	def LoadParamValue(self, tbl):
		val = tbl[self.ParamName, 1]
		if val is not None:
			self.ParamValue = float(val)


class VjzParam(VjzParamBase):
	def __init__(self, comp):
		self._comp = comp
		page = comp.appendCustomPage('Vjzparam')
		page.appendStr('Paramname', label='Parameter Name')
		page.appendToggle('Scale', label='Scale Parameter Value')
		minmax = page.appendFloat('Scalerange', label='Scale Min/Max', size=2)
		minmax[0].default = 0
		minmax[1].default = 1

	@staticmethod
	def get(comp):
		if _safeTestForAttr(comp, 'ParamDef'):
			return comp
		if _safeTestForAttr(comp, 'paramDef'):
			print('could only find VjzParam extension for comp ' + comp.path + ' using old attribute name')
			return comp
		if comp.ext and hasattr(comp.ext, 'VjzParam'):
			print('could only find VjzParam extension for comp ' + comp.path + ' using ext.VjzParam')
			return comp.ext.VjzParam
		if comp.extensions:
			for e in comp.extensions:
				if isinstance(e, VjzParam):
					print('could only find VjzParam extension for comp ' + comp.path + ' by looping through extension list')
					return e
		print('unable to find VjzParam extension for comp: ' + comp.path)
		return None

	@_override
	def PVar(self, name):
		return self._comp.var(name)

	@property
	def ParamDef(self):
		d = self._comp.op(self.PVar('pdef'))
		return d if d.numRows == 2 else None

	@_override
	def GetParamDefProperty(self, name):
		pdef = self.ParamDef
		cell = pdef[name, 1] if pdef else None
		if cell:
			return cell.val

	@_override
	def ParamValue_getter(self):
		return self._comp.op('value')[0][0]

	@_override
	def ParamValue_setter(self, val):
		self._comp.op('slider').panel.u = val

	ParamValue = property(ParamValue_getter, ParamValue_setter)

	@property
	def ParamMidiMapping(self):
		mapping = self._comp.op('mapping')
		return mapping if mapping.numRows == 2 else None

	@_override
	def ParamMidiName_getter(self):
		m = self.ParamMidiMapping
		return m[1, 'name'].val if m else None

	@_override
	def ParamMidiName_setter(self, name):
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

	ParamMidiName = property(ParamMidiName_getter, ParamMidiName_setter)

	@_override
	def UpdateParamTableEntry(self, vals):
		updateTableRow(self.PVar('editableparamtbl'), self.ParamName, vals)

	@_override
	def SaveParamMidiMapping(self):
		mapping = self.ParamMidiMapping
		if not mapping:
			dev, ctl = '', ''
		else:
			dev, ctl = mapping[1, 'mididev'].val, mapping[1, 'midictl'].val
		self.UpdateParamTableEntry({'mididev': dev, 'midictl': ctl})


class VjzModule:
	def __init__(self, comp):
		self._comp = comp
		page = comp.appendCustomPage('Vjzmodule')
		page.appendStr('Modname', label='Module name')
		callbacks = self._comp.op('callbacks')
		if callbacks and callbacks.isDAT:
			self._callbacks = mod(callbacks)
		else:
			self._callbacks = None
		toggleTag(self._comp, 'vjzmodule', self.MVar('modfake') != '1')

	@staticmethod
	def get(comp):
		if _safeTestForAttr(comp, 'ModName'):
			return comp
		if _safeTestForAttr(comp, 'modName'):
			print('could only find VjzModule extension for comp ' + comp.path + ' using old attribute name')
			return comp
		if comp.ext and hasattr(comp.ext, 'VjzModule'):
			print('could only find VjzModule extension for comp ' + comp.path + ' using ext.VjzModule')
			return comp.ext.VjzModule
		if comp.extensions:
			for e in comp.extensions:
				if isinstance(e, VjzModule):
					print('could only find VjzModule extension for comp ' + comp.path + ' by looping through extension list')
					return e
		print('unable to find VjzModule extension for comp: ' + comp.path)
		return None

	def _InvokeCallback(self, name, *args):
		if not self._callbacks or not hasattr(self._callbacks, name):
			return None
		return getattr(self._callbacks, name)(self, *args)

	def MVar(self, name):
		return self._comp.var(name)

	@property
	def ModName(self):
		return self.MVar('modname')

	@property
	def ModPath(self):
		return self._comp.path

	@property
	def ModState(self):
		return self._comp.op(self.MVar('modstate'))

	@property
	def ModParamTable(self):
		return self._comp.op(self.MVar('modparamtbl'))

	@property
	def ModParamNames(self):
		return [c.val for c in self.ModParamTable.col('name')[1:]]

	@property
	def ModParamLocalNames(self):
		return [c.val for c in self.ModParamTable.col('localname')[1:]]

	@property
	def ModParamObjects(self):
		pnames = self.ModParamLocalNames
		for p in pnames:
			pop = self.ModParam(p)
			if not pop:
				print('parameter component not found for param "' + p + '" in module "' + self.ModName + '"')
			yield pop

	def ModParam(self, name):
		pop = self._comp.op(name + '_param')
		return VjzParam.get(pop) if pop else None

	def SaveParamValues(self, tbl):
		tbl = argToOp(tbl)
		print('saving module ' + self.ModName + ' to ' + tbl.path)
		pnames = self.ModParamLocalNames
		for pname in pnames:
			self._SaveParamValue(tbl, pname)

	def _SaveParamValue(self, tbl, pname):
		if self._InvokeCallback('SaveParamValue', tbl, pname) is True:
			return
		pop = self.ModParam(pname)
		if pop:
			pop.SaveParamValue(tbl)
			return
		pvals = self._comp.op(self.MVar('modparamsout'))
		if pvals:
			c = pvals.chan(pname)
			if c is not None:
				updateTableRow(tbl, pname, {'value': c[0]})
				return
		print('cannot save parameter ' + pname)

	def LoadParamValues(self, tbl):
		tbl = argToOp(tbl)
		pnames = self.ModParamLocalNames
		for pname in pnames:
			self._LoadParamValue(tbl, pname)

	def _LoadParamValue(self, tbl, pname):
		if self._InvokeCallback('LoadParamValue', tbl, pname) is True:
			return
		pop = self.ModParam(pname)
		if pop:
			pop.LoadParamValue(tbl)
		else:
			print('cannot load parameter ' + self.ModPath + ' : ' + pname)

	def ResetParamsToDefaults(self):
		for p in self.ModParamObjects:
			p.ResetParamToDefault()

class VjzSystem:
	def __init__(self, root):
		self._root = root

	def SVar(self, name):
		return self._root.var(name)

	@property
	def ModuleTable(self):
		return self._root.op(self.SVar('moduletbl'))

	@property
	def ParamTable(self):
		return self._root.op(self.SVar('paramtbl'))

	def GetModules(self, fakes=False):
		# if not fakes:
		# 	return self._root.findChildren(tags=['vjzmodule'])
		modtbl = self.ModuleTable
		mods = []
		for mname in modtbl.col('name')[1:]:
			if not fakes and modtbl[mname, 'fake'] == '1':
				continue
			mop = self._root.op(modtbl[mname, 'path'])
			if mop:
				m = VjzModule.get(mop)
				if m:
					mods.append(m)
		return mods

	def GetModule(self, name):
		m = self.ModuleTable[name, 'path']
		m = op(m) if m else None
		if m is None:
			raise Exception('module not found: "' + name + '"')
		return VjzModule.get(m)

	def SaveParamValues(self):
		tbl = self._root.op(self.SVar('paramstatetbl'))
		for m in self.GetModules():
			m.SaveParamValues(tbl)
		tbl.save(tbl.par.file.val)

	def LoadParamValues(self):
		tbl = self._root.op(self.SVar('paramstatetbl'))
		for m in self.GetModules():
			print('loading param values in: ', m.ModPath)
			m.LoadParamValues(tbl)

	def SaveParamTableJson(self):
		tbl = self._root.op(self.SVar('editableparamtbl'))
		objs = rowsToDictList(tbl)
		j = json.dumps(objs, indent=2)
		jdat = self._root.op(self.SVar('editableparamtbljson'))
		jdat.text = j
		jdat.par.write.pulse(1)

VJZ = VjzSystem(op('/_'))