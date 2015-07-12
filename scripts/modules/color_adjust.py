def LoadParamValue(module, tbl, pname):
	if not pname in ['invert']:
		return
	fullname = module.ModName + ':' + pname
	val = tbl[fullname, 1]
	if val is None or val == '':
		return
	if pname == 'invert':
		op('invert_toggle/button').panel.state = 1 if float(val) > 0.5 else 0
		return True

def SaveParamValue(module, tbl, pname):
	if not pname in ['invert']:
		return
	fullname = module.ModName + ':' + pname
	val = None
	if pname == 'invert':
		val = 1 if op('invert_toggle/out1')[0][0] > 0.5 else 0
	if val is None:
		return
	mod.vjzual.updateTableRow(tbl, fullname, {'value': val}, addMissing=True)
	return True