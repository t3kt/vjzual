def cook(dat):
	dat.clear()
	mods = dat.inputs[0]
	dat.appendRow(['name', 'label', 'path', 'type'])
	for m in mods.col('name')[1:]:
		mname = mods[m, 'name']
		dat.appendRow([mname + ':dry'])
		dat[mname+':dry', 'label'] = mname + ' in'
		dat[mname+':dry', 'path'] = mods[m, 'dry']
		dat[mname+':dry', 'type'] = 'nodein'
		dat.appendRow([mname + ':wet'])
		dat[mname+':wet', 'label'] = mname + ' out'
		dat[mname+':wet', 'path'] = mods[m, 'wet']
		dat[mname+':wet', 'type'] = 'nodeout'
	return
