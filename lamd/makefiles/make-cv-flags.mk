# This file checks the header of the base file for information about how to produce the CV and stores it in relevant files.

# Choose mdfield implementation: mdfield-server (fast) or mdfield (compatible)
# Set LAMD_USE_SERVER_CLIENT=1 to use shell client (8x faster)
# Default: mdfield (for backward compatibility)
ifeq ($(LAMD_USE_SERVER_CLIENT),1)
    MDFIELD = $(SCRIPTDIR)/mdfield-server
else
    MDFIELD = mdfield
endif

# Extract the date and the prefix of the produced files.
DATE=$(shell $(MDFIELD) date ${BASE}.md)

CATEGORIES=$(shell $(MDFIELD) categories ${BASE}.md)

# Get macros path from frontmatter or use default
MACROSDIR=$(shell $(MDFIELD) macrosdir ${BASE}.md)

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

POSTSHEADER=$(shell $(MDFIELD) postssheader ${BASE}.md)
ASSIGNMENT=$(shell $(MDFIELD) assignment ${BASE}.md)
NOTATION=talk-notation.tex

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=inkscape #/Applications/Inkscape.app/Contents/Resources/bin/inkscape
PP=mdpp
FIND=gfind

PPFLAGS=-T --macros=$(MACROSDIR)
PPFLAGS=$(shell flags pp $(BASE)) --macros=$(MACROSDIR)

BIBDIRECTORY=$(shell $(MDFIELD) bibdir ${BASE}.md)

# Bibliography information
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

CVDIR=$(shell $(MDFIELD) cvdir $(BASE).md)

TALKSINCE=$(shell $(MDFIELD) talksince ${BASE}.md)
MEETINGSINCE=$(shell $(MDFIELD) meetingsince ${BASE}.md)
PUBLICATIONSINCE=$(shell $(MDFIELD) publicationsince $(BASE).md)

SINCEFLAGS=--meta-data talkYearSince=${TALKSINCE} meetingYearSince=${MEETINGSINCE} publicationYearSince=${PUBLICATIONSINCE}

DEPS=$(shell dependencies inputs $(BASE).md)
DIAGDEPS=$(shell dependencies diagrams $(BASE).md)
# BIBDEPS=$(shell dependencies bibinputs $(BASE).md)

POSTFLAGS=$(shell flags post $(BASE))
PPTXFLAGS=$(shell flags pptx $(BASE))
DOCXFLAGS=$(shell flags docx $(BASE))
SFLAGS=$(shell flags reveal $(BASE))

SNIPPETSDIR=$(shell $(MDFIELD) snippetsdir $(BASE).md)
DIAGRAMSDIR=$(shell $(MDFIELD) diagramsdir $(BASE).md)
WRITEDIAGRAMSDIR=$(shell $(MDFIELD) writediagramsdir $(BASE).md)
POSTSDIR=$(shell $(MDFIELD) postsdir $(BASE).md)
NOTESDIR=$(shell $(MDFIELD) notesdir $(BASE).md)
NOTEBOOKSDIR=$(shell $(MDFIELD) notebooksdir $(BASE).md)
SLIDESDIR=$(shell $(MDFIELD) slidesdir $(BASE).md)
TEXDIR=$(shell $(MDFIELD) texdir $(BASE).md)
WEEK=$(shell $(MDFIELD) week $(BASE).md)
SESSION=$(shell $(MDFIELD) session $(BASE).md)

TALKSDIR=$(shell $(MDFIELD) talksdir $(BASE).md)
PUBLICATIONSDIR=$(shell $(MDFIELD) publicationsdir $(BASE).md)
GROUPDIR=$(shell $(MDFIELD) groupdir $(BASE).md)
DATADIR=$(shell $(MDFIELD) datadir $(BASE).md)
PROJECTSDIR=$(shell $(MDFIELD) projectsdir $(BASE).md)

TALKLISTFILES=$(shell ${FIND} ${TALKSDIR} -type f)
PUBLICATIONLISTFILES=$(shell ${FIND} ${PUBLICATIONSDIR} -type f)
TEACHINGLISTFILES=${PROJECTSDIR}/teaching.yaml
PROJECTLISTFILES=${PROJECTSDIR}/grants.yaml
MEETINGLISTFILES=${PROJECTSDIR}/workshops.yaml
GROUPLISTFILES=$(shell ${FIND} ${GROUPDIR} -type f)  
EXSTUDENTFILES=${DATADIR}/students.yaml
EXRAFILES=${DATADIR}/ras.yaml

# Get all dependencies
DYNAMIC_DEPS=$(shell dependencies all $(BASE).md --snippets-path $(SNIPPETSDIR))
ALL := $(BASE).docx $(DYNAMIC_DEPS)

# Add directory check targets
.PHONY: check-snippetsdir
check-snippetsdir:
	@if [ -z "$(SNIPPETSDIR)" ]; then \
		echo "Error: 'snippetsdir' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'snippetsdir' entry pointing to your code snippets directory."; \
		echo "Example:"; \
		echo "snippetsdir: ../_snippets"; \
		exit 1; \
	fi

.PHONY: check-postsdir
check-postsdir:
	@if [ -z "$(POSTSDIR)" ]; then \
		echo "Error: 'postsdir' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'postsdir' entry pointing to your posts directory."; \
		echo "Example:"; \
		echo "postsdir: ../_posts"; \
		exit 1; \
	fi

.PHONY: check-bibdir
check-bibdir:
	@echo "Checking for bibliography files...";
	@if [ -z "$(BIBDIRECTORY)" ]; then \
		echo "Error: 'bibdir' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'bibdir' entry pointing to your bibliography directory."; \
		echo "Example:"; \
		echo "bibdir: ../_bibliography"; \
		exit 1; \
	fi

# Check if macros field is defined
.PHONY: check-macros
check-macros:
	@if [ -z "$(MACROSDIR)" ]; then \
		echo "Error: 'macrosdir' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'macrosdir' entry pointing to your macros directory."; \
		echo "Example:"; \
		echo "macrosdir: macros"; \
		exit 1; \
	fi

# Add check-macros to the all target
all: check-snippetsdir check-postsdir check-bibdir check-macros $(ALL)
