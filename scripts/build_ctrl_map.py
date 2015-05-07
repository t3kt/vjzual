def cook(dat):
	dat.clear()
	dat.appendRow(['name', 'mididev', 'midictl', 'cc', 'map'])
	addctls(dat, 'twister', '/_/local/twistermap_in', op('twisterctrlmap'))
	addctls(dat, 'codev2', '/_/local/codemap_in', op('codectrlmap'))
	return

def addctls(dat, device, mappath, tbl):
	for ctl in tbl.col('midictl')[1:]:
		name = device + ':' + ctl.val
		dat.appendRow([name])
		dat[name, 'mididev'] = device
		dat[name, 'midictl'] = ctl
		dat[name, 'cc'] = tbl[ctl, 'cc']
		dat[name, 'map'] = mappath
	pass