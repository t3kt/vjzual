def LoadParamValue(module, tbl, pname):
	if not pname in ['xfade']:
		return
	fullname = module.ModName + ':' + pname
	#print('Called LoadParamValue callback', 'pname=', pname, 'fullname=', fullname, 'module=', module, 'me=', me, 'tbl=', tbl)
	val = tbl[fullname, 1]
	if val is None or val == '':
		return
	if pname == 'xfade':
		op('blend').par.Xfade = float(val)
		return True

def SaveParamValue(module, tbl, pname):
	if not pname in ['xfade']:
		return
	fullname = module.ModName + ':' + pname
	val = None
	if pname == 'xfade':
		val = op('blend').par.Xfade
	if val is None:
		return
	mod.vjzual.updateTableRow(tbl, fullname, {'value': val}, addMissing=True)
	return True