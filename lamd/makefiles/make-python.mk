
%.plots.py.markdown: %.md ${DEPS}
	${PP} $< -o $@  --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --format code --to python --code plot ${PPFLAGS} 

%.all.py.markdown: %.md ${DEPS}
	${PP} $< -o $@  --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --format code --to python --code diagnostic ${PPFLAGS} 

${BASE}.py: ${BASE}.plots.py.markdown
	cp $< $@

${BASE}_all.py: ${BASE}.all.py.markdown
	cp $< $@
