# Check header for which formats to create in notes and slides.
# Create PDF of reveal slides with something like decktape https://github.com/astefanutti/decktape

OUT=$(PREFIX)$(BASE)

all: $(ALL)

##${BASE}.notes.tex ${BASE}.notes.pdf 


include ../make-tex.mk
include ../make-docx.mk


clean:
	rm *.markdown
	rm *.markdown-e
	rm ${ALL}
