# Check header for which formats to create in notes and slides.
# Create PDF of reveal slides with something like decktape https://github.com/astefanutti/decktape

OUT=$(PREFIX)$(BASE)

all: $(ALL)

##${BASE}.notes.tex ${BASE}.notes.pdf 


include $(INCLUDEDIR)/make-figures.mk
include $(INCLUDEDIR)/make-python.mk
include $(INCLUDEDIR)/make-slides.mk 
include $(INCLUDEDIR)/make-notes.mk
include $(INCLUDEDIR)/make-tex.mk
include $(INCLUDEDIR)/make-paper.mk
include $(INCLUDEDIR)/make-post.mk
include $(INCLUDEDIR)/make-docx.mk
include $(INCLUDEDIR)/make-ipynb.mk


clean:
	rm *.markdown
	rm *.markdown-e
	rm ${ALL}
