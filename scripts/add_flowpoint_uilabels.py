def cook(dat):
	dat.clear()
	indat = dat.inputs[0]
	dat.appendRow(indat.row(0) + ['uilabel'])
	for i in range(1, indat.numRows):
		uilabel = '%s [%s]' % (indat[i, 'label'], indat[i, 'type'])
		dat.appendRow(indat.row(i) + [uilabel])
