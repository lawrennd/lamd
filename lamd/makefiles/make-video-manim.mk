# Manim continuous video pipeline (raw Manim → MP4)
# Preprocessing: markdown → Python (raw Manim Scene subclass)
%.manim-video.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim-video --format slides --code none ${PPFLAGS} \
		--snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR}

# Render with raw manim and copy output MP4
${BASE}.manim-video.mp4: ${BASE}.manim-video.py
	manim render ${MANIMFLAGS} $< Talk -ql
	cp media/videos/${BASE}.manim-video/480p15/Talk.mp4 $@

.PHONY: manim-video
manim-video: ${BASE}.manim-video.mp4
