def cook(dat):
	dat.copy(dat.inputs[0])
	defs = dat.inputs[1]
	for c in defs.col(0):
		if dat[0, c] is None:
			dat.appendCol(c)
	cols = [c.val for c in dat.row(0)[1:]]
	for mname in dat.col('name')[1:]:
		fmtvars = {'m': dat[mname, 'path'], 'mname': mname}
		for c in cols:
			cell = dat[mname, c]
			val = cell.val
			if val == '':
				if defs[c, 1] is None:
					continue
				val = defs[c, 1].val
			if '{' in val:
				cell.val = val.format(**fmtvars)
			else:
				cell.val = val
