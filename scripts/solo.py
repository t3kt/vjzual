mods = op(me.var('moduletbl'))
target = me.var('arg1')
is_on = me.var('arg2') == 'on'
set_outsel = op('/_/mainout_selector/set')
for m in mods.col('name')[1:]:
	if mods[m, 'fake'] == '1':
		continue
	print('updating solo state for module "' + m + '"')
	if not is_on:
		m_on = False
	elif m == target:
		m_on = True
		set_outsel.run(mods[m, 'name'] + ':wet')
	else:
		m_on = False
	print('module "' + m + '" path:', mods[m, 'path'])
	btn = op(mods[m, 'path'] + '/module_header/solo_button')
	if btn:
		btn.panel.state = 1 if m_on else 0

if not is_on:
	set_outsel.run('master:wet')