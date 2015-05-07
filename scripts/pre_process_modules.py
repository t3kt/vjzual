def isTypeMatch(defmodtype, modtype):
	if defmodtype == '':
		return True
	if '|' in defmodtype:
		dtypes = defmodtype.split('|')
		return modtype in dtypes
	return defmodtype == modtype

def getDefault(defaults, propname, modtype):
	for i in range(1, defaults.numRows):
		if defaults[i, 'property'] != propname:
			continue
		if not isTypeMatch(defaults[i, 'type'].val, modtype):
			continue
		return defaults[i, 'value'].val
	return ''

def cook(dat):
	dat.copy(dat.inputs[0])
	defs = dat.inputs[1]
	for c in defs.col(0):
		if dat[0, c] is None:
			dat.appendCol(c)
	cols = [c.val for c in dat.row(0)[1:]]
	for mname in dat.col('name')[1:]:
		fmtvars = {'m': dat[mname, 'path'], 'mname': mname}
		mtype = dat[mname, 'type'].val
		for c in cols:
			cell = dat[mname, c]
			val = cell.val
			if val == '':
				val = getDefault(defs, c, mtype)
			if val == '-':
				cell.val = ''
			elif '{' in val:
				cell.val = val.format(**fmtvars)
			else:
				cell.val = val