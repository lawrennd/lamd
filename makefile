BASE=neil-lawrence_professorial-pay-review
MAKEFILESDIR=/Users/neil/lawrennd/lamd/lamd/makefiles
INCLUDESDIR=/Users/neil/lawrennd/lamd/lamd/includes
SCRIPTDIR=/Users/neil/lawrennd/lamd/lamd/scripts
include $(MAKEFILESDIR)/make-cv-flags.mk
include $(MAKEFILESDIR)/make-cv.mk

%.md: %.markdown
	$(PP) $(PPFLAGS) $< > $@
