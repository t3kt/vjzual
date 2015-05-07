def cook(dat):
	dat.clear()
	mods = dat.inputs[0]
	dat.appendRow(['name', 'label', 'path', 'type'])
	for mname in mods.col('name')[1:]:
		if mods[mname, 'fake'] == '1':
			continue
		modtype = mods[mname, 'type']
		if modtype == 'filter':
			mod.vjzual.updateTableRow(dat, mname + ':dry', {
				'label': mname + ' in',
				'path': mods[mname, 'dry'],
				'type': 'nodein'
			}, addMissing=True)
		mod.vjzual.updateTableRow(dat, mname + ':wet', {
			'label': mname + ' out',
			'path': mods[mname, 'wet'],
			'type': 'nodeout'
		}, addMissing=True)
	return
