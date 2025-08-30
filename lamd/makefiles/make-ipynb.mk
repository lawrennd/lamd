# Validation script for detecting notedown failures
# Usage: ${LAMDDIR}/scripts/validate_notebook.sh <notebook_file> <expected_min_cells>
# The script will fail the build if the notebook has insufficient cells

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
	# If notedown is re-enabled, add validation here:
	# ${LAMDDIR}/scripts/validate_notebook.sh ${BASE}.ipynb 9 || (echo "WARNING: Notedown may have failed" && exit 1)
	cp ${BASE}.ipynb ${NOTEBOOKSDIR}/${OUT}.ipynb
	rm ${BASE}.tmp.markdown

${BASE}.full.ipynb: ${BASE}.full.ipynb.markdown
	pandoc  --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-ipynb-template \
		--markdown-headings=atx \
		--out ${BASE}.tmp.markdown  ${BASE}.full.ipynb.markdown
	pandoc 	${PDSFLAGS} \
		--out $@ ${BASE}.tmp.markdown
	#notedown ${BASE}.tmp.markdown > ${BASE}.ipynb
	# If notedown is re-enabled, add validation here:
	# ${LAMDDIR}/scripts/validate_notebook.sh ${BASE}.full.ipynb 9 || (echo "WARNING: Notedown may have failed" && exit 1)
	cp ${BASE}.full.ipynb ${NOTEBOOKSDIR}/${OUT}.full.ipynb
	rm ${BASE}.tmp.markdown

${BASE}.slides.ipynb: ${BASE}.slides.ipynb.markdown
	pandoc  --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-ipynb-template \
		--markdown-headings=atx \
		${CITEFLAGS} \
		--out ${BASE}.tmp.markdown  ${BASE}.slides.ipynb.markdown
	notedown ${BASE}.tmp.markdown > ${BASE}.slides.ipynb
	# Validate that notedown created sufficient cells (expected: 9+ for typical content)
	# Note: With the fixed pandoc template, pandoc should work correctly, but notedown is still used here
	${LAMDDIR}/scripts/validate_notebook.sh ${BASE}.slides.ipynb 9 || (echo "WARNING: Notebook conversion may have failed to create proper cell boundaries" && exit 1)
	cp ${BASE}.slides.ipynb ${NOTEBOOKSDIR}/${OUT}.slides.ipynb
	rm ${BASE}.tmp.markdown
