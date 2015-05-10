def cook(dat):
	dat.clear()
	tfilter = op('define')['typefilter', 1].val
	mfilter = op('define')['modtypefilter', 1].val
	tfilter = mod.vjzual.prepFilterList(tfilter)
	mfilter = mod.vjzual.prepFilterList(mfilter)
	indat = dat.inputs[0]
	if not tfilter and not mfilter:
		dat.copy(indat)
	else:
		dat.appendRow(indat.row(0))
		for i in range(1, indat.numRows):
			t = indat[i, 'type'].val
			m = indat[i, 'modtype'].val
			if tfilter and not t in tfilter:
				continue
			if mfilter and not m in mfilter:
				continue
			dat.appendRow(indat.row(i))
