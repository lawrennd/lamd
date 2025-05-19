# Check header for which formats to create in notes and slides.
# Create PDF of reveal slides with something like decktape https://github.com/astefanutti/decktape

OUT=$(PREFIX)$(BASE)

.PHONY: all
all: check-snippetsdir check-postsdir check-bibdir 
	$(MAKE) $(BASE).docx

%.md: %.markdown
	$(PP) $(PPFLAGS) $< > $@

##${BASE}.notes.tex ${BASE}.notes.pdf 


include $(MAKEFILESDIR)/make-tex.mk
include $(MAKEFILESDIR)/make-docx.mk


clean:
	rm *.markdown
	rm *.markdown-e
	rm ${ALL}
