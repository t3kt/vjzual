for m in op('feedback_modules').col(0):
	fbk = op(m + '/feedback')
	if fbk:
		mod.vjzual.toggleBypass(fbk, delayFrames=1)
	comp = op(m + '/feedback_comp')
	if comp:
		mod.vjzual.toggleBypass(comp, delayFrames=2)
		run('op("'+comp.path+'").cook(force=True)', delayFrames=3)