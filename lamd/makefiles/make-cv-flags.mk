# This file checks the header of the base file for information about how to produce the talk and stores it in relevant files.

# Extract the date and the prefix of the produced files.
DATE=$(shell mdfield date ${BASE}.md)

CATEGORIES=$(shell mdfield categories ${BASE}.md)

# Get macros path from frontmatter or use default
MACROS=$(shell mdfield macros ${BASE}.md)
MACROS?=macros

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

POSTSHEADER=$(shell mdfield postssheader ${BASE}.md)
ASSIGNMENT=$(shell mdfield assignment ${BASE}.md)
NOTATION=talk-notation.tex

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=inkscape #/Applications/Inkscape.app/Contents/Resources/bin/inkscape
PP=mdpp
FIND=gfind

PPFLAGS=-T --macros=$(MACROS)
PPFLAGS=$(shell flags pp $(BASE)) --macros=$(MACROS)

BIBDIRECTORY=$(shell mdfield bibdir ${BASE}.md)

# Bibliography information
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

CVDIR=$(shell mdfield cvdir $(BASE).md)

TALKSINCE=$(shell mdfield talksince ${BASE}.md)
MEETINGSINCE=$(shell mdfield meetingsince ${BASE}.md)
PUBLICATIONSINCE=$(shell mdfield publicationsince $(BASE).md)

SINCEFLAGS=--meta-data talkYearSince=${TALKSINCE} meetingYearSince=${MEETINGSINCE} publicationYearSince=${PUBLICATIONSINCE}

DEPS=$(shell dependencies inputs $(BASE).md)
DIAGDEPS=$(shell dependencies diagrams $(BASE).md)
# BIBDEPS=$(shell dependencies bibinputs $(BASE).md)

POSTFLAGS=$(shell flags post $(BASE))
PPTXFLAGS=$(shell flags pptx $(BASE))
DOCXFLAGS=$(shell flags docx $(BASE))
SFLAGS=$(shell flags reveal $(BASE))

SNIPPETSDIR=$(shell mdfield snippetsdir $(BASE).md)
DIAGRAMSDIR=$(shell mdfield diagramsdir $(BASE).md)
WRITEDIAGRAMSDIR=$(shell mdfield writediagramsdir $(BASE).md)
POSTSDIR=$(shell mdfield postsdir $(BASE).md)
NOTESDIR=$(shell mdfield notesdir $(BASE).md)
NOTEBOOKSDIR=$(shell mdfield notebooksdir $(BASE).md)
SLIDESDIR=$(shell mdfield slidesdir $(BASE).md)
TEXDIR=$(shell mdfield texdir $(BASE).md)
WEEK=$(shell mdfield week $(BASE).md)
SESSION=$(shell mdfield session $(BASE).md)

TALKSDIR=$(shell mdfield talksdir $(BASE).md)
PUBLICATIONSDIR=$(shell mdfield publicationsdir $(BASE).md)
GROUPDIR=$(shell mdfield groupdir $(BASE).md)
DATADIR=$(shell mdfield datadir $(BASE).md)
PROJECTSDIR=$(shell mdfield projectsdir $(BASE).md)

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
	@if [ -z "$(MACROS)" ]; then \
		echo "Error: 'macros' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'macros' entry pointing to your macros directory."; \
		echo "Example:"; \
		echo "macros: macros"; \
		exit 1; \
	fi

# Add check-macros to the all target
all: check-snippetsdir check-postsdir check-bibdir check-macros $(ALL)
