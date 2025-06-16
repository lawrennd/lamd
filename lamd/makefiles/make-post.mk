${BASE}.posts.html.markdown: ${BASE}.md ${DEPS}
	${PP} $< -o $@ --format notes --to html --code sparse --snippets-path ${SNIPPETSDIR} --replace-notation --edit-links --exercises ${PPFLAGS} 

${BASE}.posts.html: ${BASE}.posts.html.markdown
	pandoc --template ${TEMPLATESDIR}/pandoc/pandoc-jekyll-talk-template ${PDSFLAGS} \
	       --markdown-headings=atx \
	       ${POSTFLAGS} \
               --to html \
               --out ${BASE}.posts.html  ${BASE}.posts.html.markdown 
	cp ${BASE}.posts.html ${POSTSDIR}/${OUT}.html
	${SCRIPTDIR}/copy_web_diagrams.sh ${VERBOSE:+--verbose} ${BASE}.md slidediagrams ${SLIDESDIR}/diagrams/ ${SLIDESDIR} ${DIAGRAMSDIR} ${SNIPPETSDIR}

