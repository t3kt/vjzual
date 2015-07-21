mod.vjzual.DEBUGLOG('executing init for: ' + op('..').path)
# page = parent().appendCustomPage('Vjzmodule')
# page.appendStr('Modname', label='Module name')
for i in ops('*/init'):
	try:
		i.run()
	except Exception as e:
		print('INIT error for ' + i, e)
