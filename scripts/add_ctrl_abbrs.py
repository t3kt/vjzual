def cook(dat):
	dat.clear()
	dat.copy(dat.inputs[0])
	dat.insertCol(['abbr'])
	for i in range(1, dat.numRows):
		name = dat[i, 'name'].val
		if ':' in name:
			dev, ctl = name.split(':')
			abbr = dev[0] + ':' + ctl
		else:
			abbr = name
		dat[i, 'abbr'] = abbr
	return
