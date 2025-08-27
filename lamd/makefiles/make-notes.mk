%.notes.html.markdown: %.md ${DEPS}
	${PP} $< -o $@  --format notes --to html --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR} --replace-notation --edit-links --exercises ${PPFLAGS} 

%.notes.docx.markdown: %.md ${DEPS}
	${PP} $< -o $@ --format notes --to docx --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --replace-notation --edit-links ${PPFLAGS}
	echo ${BASE}


${BASE}.notes.html: ${BASE}.notes.html.markdown ${BIBDEPS}
	pandoc  ${PDSFLAGS} \
		--mathjax \
		-o ${BASE}.notes.html  \
		${BASE}.notes.html.markdown
	@if [ "$(LAYOUT)" = "practical" ] && [ -n "$(PRACTICALSDIR)" ]; then \
		cp ${BASE}.notes.html ${PRACTICALSDIR}/${OUT}.notes.html; \
		echo "Copied ${BASE}.notes.html to ${PRACTICALSDIR}/${OUT}.notes.html"; \
	fi 

