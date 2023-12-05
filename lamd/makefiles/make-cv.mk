# Check header for which formats to create in notes and slides.
# Create PDF of reveal slides with something like decktape https://github.com/astefanutti/decktape

OUT=$(PREFIX)$(BASE)

all: $(ALL)

##${BASE}.notes.tex ${BASE}.notes.pdf 


include $(MAKEFILESDIR)/make-lists.mk
include $(MAKEFILESDIR)/make-tex.mk
include $(MAKEFILESDIR)/make-docx.mk


clean:
	rm *.markdown
	rm *.markdown-e
	rm ${ALL}
