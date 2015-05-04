def cook(dat):
	dat.copy(dat.inputs[0])
	defs = dat.inputs[1]
	modtbl = dat.inputs[2]
	for c in defs.col(0):
		if dat[0, c] is None:
			dat.appendCol(c)
	cols = [c.val for c in dat.row(0)[1:]]
	for pname in dat.col('name')[1:]:
		mname = dat[pname, 'module']
		fmtvars = {'m': modtbl[mname, 'path'], 'plocal': dat[pname, 'localname']}
		if not fmtvars['m']:
			fmtvars['m'] = ''
		if not fmtvars['plocal']:
			fmtvars['plocal'] = ''
		for c in cols:
			cell = dat[pname, c]
			val = cell.val
			if val == '':
				if defs[c, 1] is None:
					continue
				val = defs[c, 1].val
			if '{' in val:
				cell.val = val.format(**fmtvars)
			else:
				cell.val = val
