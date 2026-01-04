%.notes.docx.markdown: %.md ${DEPS}
	${PP} $< -o $@ --format notes --to docx --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR} --edit-links ${PPFLAGS} --replace-notation

# Direct rule for CV generation with preprocessing
${BASE}.preprocessed.md: ${BASE}.md ${DEPS}
	${PP} $< -o $@ --format notes --to docx --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR} --edit-links ${PPFLAGS} --replace-notation

${BASE}.docx: ${BASE}.preprocessed.md
	pandoc -s \
		${CITEFLAGS} \
		${DOCXFLAGS} \
		-o ${BASE}.docx \
		${BASE}.preprocessed.md

# Original rule for reference
original-${BASE}.docx: ${BASE}.notes.docx.markdown ${DOCXDEPS}
	pandoc -s \
		${CITEFLAGS} \
		${DOCXFLAGS} \
		-B ${INCLUDESDIR}/${NOTATION} \
		-o ${BASE}.docx \
		${BASE}.notes.docx.markdown

