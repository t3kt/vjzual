def offToOn(panelValue):
	preview = op(me.var('preview'))
	source = op('..')
	preview.op('set_source')[0,0] = source.path
	preview.op('label/define')['label', 1] = source.name

def onToOff(panelValue):
	pass