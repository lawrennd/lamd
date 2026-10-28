# Check header for which formats to create in notes and slides.
# Slides PDF is Beamer via make-tex.mk (${BASE}.slides.pdf, CIP-0017).

OUT=$(PREFIX)$(BASE)

all: $(ALL)

##${BASE}.notes.tex ${BASE}.notes.pdf 


include $(MAKEFILESDIR)/make-figures.mk
include $(MAKEFILESDIR)/make-people.mk
include $(MAKEFILESDIR)/make-python.mk
include $(MAKEFILESDIR)/make-slides.mk 
include $(MAKEFILESDIR)/make-notes.mk
include $(MAKEFILESDIR)/make-tex.mk
include $(MAKEFILESDIR)/make-paper.mk
include $(MAKEFILESDIR)/make-post.mk
include $(MAKEFILESDIR)/make-docx.mk
include $(MAKEFILESDIR)/make-ipynb.mk
include $(MAKEFILESDIR)/make-manim.mk
include $(MAKEFILESDIR)/make-video-manim.mk
include $(MAKEFILESDIR)/make-svg-manim.mk


clean:
	rm *.markdown
	rm *.markdown-e
	rm ${ALL}
