${BASE}.posts.html.markdown: ${BASE}.md ${DEPS}
	${PP} $< -o $@ --format notes --to html --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --replace-notation --edit-links --exercises ${PPFLAGS} 

${BASE}.posts.html: ${BASE}.posts.html.markdown
	pandoc --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-talk-template ${PDSFLAGS} \
	       --markdown-headings=atx \
	       ${POSTFLAGS} \
               --to html \
               --out ${BASE}.posts.html  ${BASE}.posts.html.markdown 
	@if [ "$(LAYOUT)" = "practical" ] && [ -n "$(PRACTICALSDIR)" ]; then \
		cp ${BASE}.posts.html ${PRACTICALSDIR}/${OUT}.html; \
		echo "Copied ${BASE}.posts.html to ${PRACTICALSDIR}/${OUT}.html"; \
	else \
		cp ${BASE}.posts.html ${POSTSDIR}/${OUT}.html; \
	fi
	${SCRIPTDIR}/copy_web_diagrams.sh ${VERBOSE:+--verbose} ${BASE}.md slidediagrams ${SLIDESDIR}/diagrams/ ${SLIDESDIR} ${DIAGRAMSDIR} ${SNIPPETSDIR}

