comp = parent()
page = comp.appendCustomPage('Lookup')

def copyAttrs(par, origPar, names):
	#print('copying attrs from ', repr(origPar), ' to ', repr(par))
	for name in names:
		#print('copying attr ', name)
		val = getattr(origPar, name)
		if val is None:
			continue
		if isinstance(val, list):
			val = list(val)
		setattr(par, name, val)

def copyParAttrs(par, origPar):
	copyAttrs(par, origPar, ['menuNames', 'menuLabels', 'min', 'max', 'clampMin', 'clampMax', 'default', 'normMin', 'normMax', 'normVal'])

def copyMenuAttrs(par, origPar):
	copyAttrs(par, origPar, ['menuNames', 'menuLabels', 'default'])

tex3d = op('tex3d')
active = page.appendToggle('Active', label='Cache Active')[0]
copyParAttrs(active, tex3d.par.active)
prefill = page.appendToggle('Prefill', label='Prefill')[0]
copyParAttrs(prefill, tex3d.par.prefill)
cachesize = page.appendInt('Cachesize', label='Cache Size')[0]
copyParAttrs(cachesize, tex3d.par.cachesize)
step = page.appendInt('Step', label='Step Size')[0]
copyParAttrs(step, tex3d.par.step)
reset = page.appendToggle('Reset', label='Reset Cache')[0]
copyParAttrs(reset, tex3d.par.reset)

posMin = page.appendXYZ('Posmin', label='Minimum Position/Time')
posMin[0].default = posMin[1].default = posMin[2].default = 0
posMax = page.appendXYZ('Posmax', label='Maximum Position/Time')
posMax[0].default = posMax[1].default = posMax[2].default = 1

glsl = op('lookup_glsl')
extUV = page.appendMenu('Inputextenduv', label='Input Extend Mode UV')[0]
copyMenuAttrs(extUV, glsl.par.inputextenduv)
extUV.default = 'repeat'
extW = page.appendMenu('Inputextendw', label='Input Extend Mode Time')[0]
copyMenuAttrs(extW, glsl.par.inputextendw)
extW.default = 'repeat'

