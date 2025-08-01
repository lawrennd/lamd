%.slides.pptx.markdown: %.md ${PPTXDEPS}
	${PP} $< -o $@  --to pptx --format slides --code none ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR}  --replace-notation

%.slides.html.markdown: %.md ${DEPS}
	${PP} $< -o $@ --to html --format slides --code none ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --replace-notation


${BASE}.slides.html: ${BASE}.slides.html.markdown ${BIBDEPS}
	pandoc --template ${TEMPLATESDIR}/pandoc/pandoc-revealjs-template ${PDSFLAGS} ${SLIDEFLAGS} --include-in-header=${INCLUDESDIR}/${SLIDESHEADER} -t revealjs ${BIBFLAGS} -o ${BASE}.slides.html  ${BASE}.slides.html.markdown 
	cp ${BASE}.slides.html ${SLIDESDIR}/${OUT}.slides.html

${BASE}.pptx: ${BASE}.slides.pptx.markdown 
	pandoc  -t pptx \
		-o $@ $< \
		${PPTXFLAGS} \
		${CITEFLAGS} \
		${SLIDEFLAGS}
