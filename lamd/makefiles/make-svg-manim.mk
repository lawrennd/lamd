# SVG Manim presentation pipeline (lawrennd/manim SVG renderer)
# Produces a RevealJS HTML presentation with per-frame SVG animations
# instead of MP4 video clips (cf. make-manim.mk which uses manim-slides).
#
# Dependencies:
#   pip install "manim[svg] @ git+https://github.com/lawrennd/manim.git"
#
# Variables (override in your talk's Makefile):
#   MANIMSVGFLAGS  — extra flags passed to `manim` (e.g. -ql for low quality)
#   MANIMSVGJS     — path to js/manim-svg.js from the lawrennd/manim install

# Use low quality by default (-ql) — faster renders, smaller SVGs.
# Override with e.g. MANIMSVGFLAGS=-qh for high quality.
MANIMSVGFLAGS ?= -ql
MANIMSVGJS ?= $(shell python -c \
	"import manim, os; print(os.path.join(os.path.dirname(manim.__file__), '..', 'js', 'manim-svg.js'))" \
	2>/dev/null)

# Preprocess: markdown → Python scene (standard Manim Scene + SVG renderer)
%.manim-svg.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim-svg --format slides --code none ${PPFLAGS} \
		--snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) \
		--diagrams-dir ${DIAGRAMSDIR}

# Render: Python → SVG frame directories under media/svg/Talk/
${BASE}.manim-svg.rendered: ${BASE}.manim-svg.py
	manim ${MANIMSVGFLAGS} --renderer svg $< Talk
	touch $@

# Generate: SVG frame directories → RevealJS HTML
${BASE}.manim-svg.html: ${BASE}.manim-svg.rendered
	python -m lamd.util.svg_to_html media/svg/Talk ${BASE}.manim-svg.html \
		--title "$(TITLE)" --js-src "$(MANIMSVGJS)"

.PHONY: manim-svg
manim-svg: ${BASE}.manim-svg.html
