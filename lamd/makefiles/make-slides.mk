%.slides.pptx.markdown: %.md ${PPTXDEPS} check-reference-docs
	${PP} $< -o $@  --to pptx --format slides --code none ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR}  --replace-notation

%.slides.html.markdown: %.md ${DEPS}
	${PP} $< -o $@ --to html --format slides --code none ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --replace-notation


# CIP-0012 Track B: optional post-Reveal.initialize fragment (only when slide_setup is set)
SLIDE_SETUP_FLAG=$(if $(strip $(SLIDESETUP)),--include-after-body=${INCLUDESDIR}/${SLIDESETUP},)

${BASE}.slides.html: ${BASE}.slides.html.markdown ${BIBDEPS}
	pandoc --template ${TEMPLATESDIR}/pandoc/pandoc-revealjs-template ${PDSFLAGS} ${SLIDEFLAGS} --include-in-header=${INCLUDESDIR}/${SLIDESHEADER} $(SLIDE_SETUP_FLAG) -t revealjs ${BIBFLAGS} -o ${BASE}.slides.html  ${BASE}.slides.html.markdown 
	cp ${BASE}.slides.html ${SLIDESDIR}/${OUT}.slides.html

${BASE}.pptx: ${BASE}.slides.pptx.markdown
	pandoc  -t pptx \
		-o $@ $< \
		${PPTXFLAGS} \
		${CITEFLAGS} \
		${SLIDEFLAGS}
