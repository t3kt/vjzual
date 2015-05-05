def cook(dat):
	dat.clear()
	mods = dat.inputs[0]
	dat.appendRow(['name', 'label', 'path', 'type'])
	for mname in mods.col('name')[1:]:
		if mods[mname, 'fake'] == '1':
			continue
		dat.appendRow([mname + ':dry'])
		dat[mname+':dry', 'label'] = mname + ' in'
		dat[mname+':dry', 'path'] = mods[mname, 'dry']
		dat[mname+':dry', 'type'] = 'nodein'
		dat.appendRow([mname + ':wet'])
		dat[mname+':wet', 'label'] = mname + ' out'
		dat[mname+':wet', 'path'] = mods[mname, 'wet']
		dat[mname+':wet', 'type'] = 'nodeout'
	return
