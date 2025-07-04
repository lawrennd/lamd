%.notes.ipynb.markdown: %.md ${DEPS}
	${PP} $< -o $@ --format notes --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --write-diagrams-dir ${WRITEDIAGRAMSDIR} --to ipynb --code ipynb --replace-notation --edit-links --exercises ${PPFLAGS} 

%.full.ipynb.markdown: %.md ${DEPS}
	${PP} $< -o $@ --format notes --to ipynb --code full --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --edit-links --replace-notation ${PPFLAGS} 

%.slides.ipynb.markdown: %.md ${DEPS}
	${PP} $< -o $@ --format slides --to ipynb --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) ${PPFLAGS} 


${BASE}.ipynb: ${BASE}.notes.ipynb.markdown
	pandoc  --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-ipynb-template \
		--markdown-headings=atx \
		--out ${BASE}.tmp.markdown  ${BASE}.notes.ipynb.markdown
	pandoc 	${PDSFLAGS} \
		--out $@ ${BASE}.tmp.markdown
	#notedown ${BASE}.tmp.markdown > ${BASE}.ipynb
	cp ${BASE}.ipynb ${NOTEBOOKSDIR}/${OUT}.ipynb
	rm ${BASE}.tmp.markdown

${BASE}.full.ipynb: ${BASE}.full.ipynb.markdown
	pandoc  --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-ipynb-template \
		--markdown-headings=atx \
		--out ${BASE}.tmp.markdown  ${BASE}.full.ipynb.markdown
	pandoc 	${PDSFLAGS} \
		--out $@ ${BASE}.tmp.markdown
	#notedown ${BASE}.tmp.markdown > ${BASE}.ipynb
	cp ${BASE}.full.ipynb ${NOTEBOOKSDIR}/${OUT}.full.ipynb
	rm ${BASE}.tmp.markdown

${BASE}.slides.ipynb: ${BASE}.slides.ipynb.markdown
	pandoc  --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-ipynb-template \
		--markdown-headings=atx \
		${CITEFLAGS} \
		--out ${BASE}.tmp.markdown  ${BASE}.slides.ipynb.markdown
	notedown ${BASE}.tmp.markdown > ${BASE}.slides.ipynb
	cp ${BASE}.slides.ipynb ${NOTEBOOKSDIR}/${OUT}.slides.ipynb
	rm ${BASE}.tmp.markdown
