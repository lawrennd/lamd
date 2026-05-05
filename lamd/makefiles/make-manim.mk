# Manim interactive presentation pipeline (manim-slides)
# Preprocessing: markdown → Python (manim-slides Slide subclass)
%.manim.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim --format slides --code none ${PPFLAGS} \
		--snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR}

# Render with manim-slides and convert to HTML
${BASE}.manim.html: ${BASE}.manim.py
	manim-slides render ${MANIMFLAGS} $< Talk -ql
	manim-slides convert ${MANIMCONVERTFLAGS} --to html Talk ${BASE}.manim.html

# Render with manim-slides and convert to PPTX
${BASE}.manim.pptx: ${BASE}.manim.py
	manim-slides render ${MANIMFLAGS} $< Talk -ql
	manim-slides convert ${MANIMCONVERTFLAGS} --to pptx Talk ${BASE}.manim.pptx

.PHONY: manim
manim: ${BASE}.manim.html ${BASE}.manim.pptx
