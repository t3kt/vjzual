def LoadParamValue(module, tbl, pname):
	if not pname in ['src', 'feedback']:
		return
	fullname = module.ModName + ':' + pname
	val = tbl[fullname, 1]
	if val is None or val == '':
		return
	if pname == 'src':
		op('src_selector').par.Src = val
		return True
	elif pname == 'feedback':
		op('src_selector').par.Feedback = float(val) > 0.5
		return True

def SaveParamValue(module, tbl, pname):
	if not pname in ['src', 'feedback']:
		return
	fullname = module.ModName + ':' + pname
	val = None
	if pname == 'src':
		val = op('src_selector').par.Src
	elif pname == 'feedback':
		val = 1 if op('src_selector').par.Feedback.val else 0
	if val is None:
		return
	mod.vjzual.updateTableRow(tbl, fullname, {'value': val}, addMissing=True)
	return True