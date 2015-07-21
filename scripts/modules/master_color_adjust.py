specialParams = [
		'mode',
		'invert1', 'invert2', 'invert3',
		'blacklevel1', 'blacklevel2', 'blacklevel3',
		'brightness11', 'brightness12', 'brightness13',
		'gamma11', 'gamma12', 'gamma13',
		'contrast1', 'contrast2', 'contrast3',
		'highr1', 'highr2', 'highr3',
		'highg1', 'highg2', 'highg3',
		'highb1', 'highb2', 'highb3',
	]
def LoadParamValue(module, tbl, pname):
	if not pname in specialParams:
		return
	fullname = module.ModName + ':' + pname
	#print('Called LoadParamValue callback', 'pname=', pname, 'fullname=', fullname, 'module=', module, 'me=', me, 'tbl=', tbl)
	val = tbl[fullname, 1]
	if val is None or val == '':
		return
	num = pname[-1]
	basename = pname[0:-1]
	if pname == 'mode':
		op('mode_radio_button/set').run(val)
		return True
	elif basename == 'invert':
		op('invert_row/ctrl_' + num + '/button').panel.state = float(val) > 0.5
		return True
	elif basename in ['blacklevel', 'brightness1', 'gamma1', 'contrast', 'highr', 'highg', 'highb']:
		op(basename + '_row/ctrl_' + num + '/string')[0, 0] = val
		return True

def SaveParamValue(module, tbl, pname):
	if not pname in specialParams:
		return
	fullname = module.ModName + ':' + pname
	num = pname[-1]
	basename = pname[0:-1]
	val = None
	if pname == 'mode':
		val = int(op('mode_radio_button/out1')[0])
	elif basename == 'invert':
		val = 1 if op('invert_row/ctrl_' + num + '/button').panel.state.val > 0.5 else 0
	elif basename in ['blacklevel', 'brightness1', 'gamma1', 'contrast', 'highr', 'highg', 'highb']:
		val = op(basename + '_row/ctrl_' + num + '/string')[0, 0].val
	if val is None:
		return
	mod.vjzual.updateTableRow(tbl, fullname, {'value': val}, addMissing=True)
	return True