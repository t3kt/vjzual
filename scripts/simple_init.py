mod.vjzual.DEBUGLOG('executing init for: ' + op('..').path)
for i in ops('*/init'):
	try:
		i.run()
	except Exception as e:
		print('INIT error for ' + i, e)
