p = parent()
mod.vjzual.DEBUGLOG('initializing parameter comp: ' + p.path)
p.par.display.expr = 'tab("./should_display", 0, 0)'
p.par.h = var('paramuih')
p.par.extension1 = 'mod.vjzual.VjzParam(me)'
p.par.promoteextension1 = 1
#p.par.reinitextensions.pulse(1)
#page = p.appendCustomPage('Vjzparam')
#page.appendStr('Paramname', label='Parameter Name')
op('midictllist/define')['displaylabel', 1] = '0'
op('midictllist/define')['hidebtn', 1] = '1'
op('midictllist/define')['font_size', 1] = '7'
op('midictllist/define')['listitems', 1] = '15'
op('midictllist/dropdown/scrollbar').par.w = 10
op('signallist/define')['displaylabel', 1] = '0'
op('signallist/define')['hidebtn', 1] = '1'
op('signallist/define')['font_size', 1] = '7'
op('signallist/define')['listitems', 1] = '15'
op('signallist/dropdown/scrollbar').par.w = 10
op('range/define')['label', 1] = ''
pdef = op(var('pdef'))
dev, ctl = pdef[1, 'mididev'], pdef[1, 'midictl']
if dev and dev.val and ctl and ctl.val:
	mname = dev.val[0] + ':' + ctl.val
	i = op('sel_midictrlmap')[mname, 0].row + 1
else:
	mname = '-'
	i = 0
op('midictllist/set').run(i, mname)
op('midictllist/script').text = ''
op('signallist/script').text = ''
mod('update_signal_sel').update(op('signal'))
if pdef[1, 'localname']:
	op('localname_text').par.text = pdef[1, 'localname'].val.replace('_', ' ')
op('slider/mid_bar_switch').par.index = 1 if pdef[1, 'showmidbar'] == '1' else 0
if pdef[1, 'scale']:
	p.par.Scale = pdef[1, 'scale'] == '1'
if pdef[1, 'scalemin']:
	p.par.Scalerange1 = float(pdef[1, 'scalemin'])
if pdef[1, 'scalemax']:
	p.par.Scalerange2 = float(pdef[1, 'scalemax'])