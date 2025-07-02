%.notes.tex.markdown: %.md ${DEPS}
	${PP} $< -o $@ --format notes --to tex --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir diagrams --edit-links ${PPFLAGS} 
	# Fix percentage width for latex.
	sed -i -e 's/width=\(.*\)\%/width=0.\1\\textwidth/g' $@
	sed -i -e 's/height=\(.*\)\%/height=0.\1\\textheight/g' $@


${BASE}.notes.pdf: ${BASE}.notes.aux ${BASE}.notes.bbl ${BASE}.notes.tex
	pdflatex -shell-escape ${BASE}.notes.tex
	cp ${BASE}.notes.pdf ${NOTESDIR}/${OUT}.notes.pdf

${BASE}.notes.bbl: ${BASE}.notes.aux ${BIBDEPS}
	bibtex ${BASE}.notes

${BASE}.notes.aux: ${BASE}.notes.tex
	pdflatex -shell-escape ${BASE}.notes.tex


${BASE}.notes.tex: ${BASE}.notes.tex.markdown 
	pandoc  -s \
		--template ${TEMPLATESDIR}/pandoc/pandoc-notes-tex-template.tex \
		--number-sections \
		--natbib \
		${BIBFLAGS} \
		-B ../_includes/${NOTATION} \
		-o ${BASE}.notes.tex  \
		${BASE}.notes.tex.markdown 

${BASE}.include.tex: ${BASE}.notes.tex.markdown ${TEXDEPS}
	pandoc  -s \
		--template ${TEMPLATESDIR}/pandoc/pandoc-include-tex-template.tex \
		--number-sections \
		--natbib \
		${BIBFLAGS} \
		-B ../_includes/${NOTATION} \
		-o ${BASE}.include.tex  \
		${BASE}.notes.tex.markdown 
	cp ${BASE}.include.tex ${TEXDIR}/${BASE}.include.tex
	${SCRIPTDIR}/copy_web_diagrams.sh ${VERBOSE:+--verbose} ${BASE}.md texdiagrams ${TEXDIR}/diagrams ${SLIDESDIR} ${DIAGRAMSDIR} ${SNIPPETSDIR}

${BASE}.tex: ${BASE}.tex.markdown
	pandoc --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-tex-template ${PDSFLAGS} \
	       --markdown-headings=atx \
	       ${TEXFLAGS} \
               --to latex \
               --out ${BASE}.tex  ${BASE}.tex.markdown 
	${SCRIPTDIR}/copy_web_diagrams.sh ${VERBOSE:+--verbose} ${BASE}.md texdiagrams ${TEXDIR}/diagrams ${SLIDESDIR} ${DIAGRAMSDIR} ${SNIPPETSDIR}
