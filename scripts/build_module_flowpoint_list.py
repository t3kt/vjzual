def cook(dat):
	dat.clear()
	mods = dat.inputs[0]
	dat.appendRow(['name', 'label', 'path', 'audiopath', 'type', 'modtype'])
	for mname in mods.col('name')[1:]:
		if mods[mname, 'fake'] == '1':
			continue
		modtype = mods[mname, 'type']
		if modtype == 'filter':
			mod.vjzual.updateTableRow(dat, mname + ':dry', {
				'label': mname + ' in',
				'path': mods[mname, 'dry'],
				'audiopath': mods[mname, 'dryaudio'],
				'type': 'nodein',
				'modtype': modtype
			}, addMissing=True)
		if modtype == 'chain' or modtype == 'filter' or modtype == 'source':
			mod.vjzual.updateTableRow(dat, mname + ':wet', {
				'label': mname + ' out',
				'path': mods[mname, 'wet'],
				'audiopath': mods[mname, 'wetaudio'],
				'type': 'nodeout',
				'modtype': modtype
			}, addMissing=True)
