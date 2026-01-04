# This file checks the header of the base file for information about how to produce the CV and stores it in relevant files.

# TIME_CMD is set by maketalk/makecv when profiling is enabled
# When profiling: TIME_CMD = $(SCRIPTDIR)/profile-command
# When normal: TIME_CMD = (empty)

# Extract all fields in one call instead of 25 separate calls
# Write batch output to temp file to avoid Make variable issues with multiline content
_FIELDS_CACHE:=$(shell mktemp)
_FIELDS_EXTRACTED:=$(shell $(TIME_CMD) mdfield batch $(BASE).md --fields date categories macrosdir postssheader assignment bibdir cvdir talksince meetingsince publicationsince snippetsdir diagramsdir writediagramsdir postsdir notesdir notebooksdir slidesdir texdir week session talksdir publicationsdir groupdir datadir projectsdir > $(_FIELDS_CACHE))

# Parse individual fields from batch output
DATE:=$(shell grep '^date:' $(_FIELDS_CACHE) | sed 's/^date://')
CATEGORIES:=$(shell grep '^categories:' $(_FIELDS_CACHE) | sed 's/^categories://')
MACROSDIR:=$(shell grep '^macrosdir:' $(_FIELDS_CACHE) | sed 's/^macrosdir://')
POSTSHEADER:=$(shell grep '^postssheader:' $(_FIELDS_CACHE) | sed 's/^postssheader://')
ASSIGNMENT:=$(shell grep '^assignment:' $(_FIELDS_CACHE) | sed 's/^assignment://')
BIBDIRECTORY:=$(shell grep '^bibdir:' $(_FIELDS_CACHE) | sed 's/^bibdir://')
CVDIR:=$(shell grep '^cvdir:' $(_FIELDS_CACHE) | sed 's/^cvdir://')
TALKSINCE:=$(shell grep '^talksince:' $(_FIELDS_CACHE) | sed 's/^talksince://')
MEETINGSINCE:=$(shell grep '^meetingsince:' $(_FIELDS_CACHE) | sed 's/^meetingsince://')
PUBLICATIONSINCE:=$(shell grep '^publicationsince:' $(_FIELDS_CACHE) | sed 's/^publicationsince://')
SNIPPETSDIR:=$(shell grep '^snippetsdir:' $(_FIELDS_CACHE) | sed 's/^snippetsdir://')
DIAGRAMSDIR:=$(shell grep '^diagramsdir:' $(_FIELDS_CACHE) | sed 's/^diagramsdir://')
WRITEDIAGRAMSDIR:=$(shell grep '^writediagramsdir:' $(_FIELDS_CACHE) | sed 's/^writediagramsdir://')
POSTSDIR:=$(shell grep '^postsdir:' $(_FIELDS_CACHE) | sed 's/^postsdir://')
NOTESDIR:=$(shell grep '^notesdir:' $(_FIELDS_CACHE) | sed 's/^notesdir://')
NOTEBOOKSDIR:=$(shell grep '^notebooksdir:' $(_FIELDS_CACHE) | sed 's/^notebooksdir://')
SLIDESDIR:=$(shell grep '^slidesdir:' $(_FIELDS_CACHE) | sed 's/^slidesdir://')
TEXDIR:=$(shell grep '^texdir:' $(_FIELDS_CACHE) | sed 's/^texdir://')
WEEK:=$(shell grep '^week:' $(_FIELDS_CACHE) | sed 's/^week://')
SESSION:=$(shell grep '^session:' $(_FIELDS_CACHE) | sed 's/^session://')
TALKSDIR:=$(shell grep '^talksdir:' $(_FIELDS_CACHE) | sed 's/^talksdir://')
PUBLICATIONSDIR:=$(shell grep '^publicationsdir:' $(_FIELDS_CACHE) | sed 's/^publicationsdir://')
GROUPDIR:=$(shell grep '^groupdir:' $(_FIELDS_CACHE) | sed 's/^groupdir://')
DATADIR:=$(shell grep '^datadir:' $(_FIELDS_CACHE) | sed 's/^datadir://')
PROJECTSDIR:=$(shell grep '^projectsdir:' $(_FIELDS_CACHE) | sed 's/^projectsdir://')

# Clean up temp file immediately after extraction
_FIELDS_CLEANUP:=$(shell rm -f $(_FIELDS_CACHE))

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

NOTATION=talk-notation.tex

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=inkscape #/Applications/Inkscape.app/Contents/Resources/bin/inkscape
PP=mdpp
FIND=gfind

PPFLAGS=-T --macros=$(MACROSDIR)
PPFLAGS=$(shell flags pp $(BASE)) --macros=$(MACROSDIR)

# Bibliography information
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

SINCEFLAGS=--meta-data talkYearSince=${TALKSINCE} meetingYearSince=${MEETINGSINCE} publicationYearSince=${PUBLICATIONSINCE}

# CIP-0009 Phase 1: Batch dependency extraction (70% faster)
# Extract all dependency types in one call instead of multiple separate calls
# Write batch output to temp file to avoid Make variable issues with multiline content
_DEPS_CACHE:=$(shell mktemp)
# Only pass --snippets-path if SNIPPETSDIR is defined (use shell conditional)
_DEPS_EXTRACTED:=$(shell if [ -n "$(SNIPPETSDIR)" ]; then $(TIME_CMD) dependencies batch $(BASE).md --snippets-path $(SNIPPETSDIR) > $(_DEPS_CACHE); else $(TIME_CMD) dependencies batch $(BASE).md > $(_DEPS_CACHE); fi)
DEPS:=$(shell grep '^inputs:' $(_DEPS_CACHE) | sed 's/^inputs://')
DIAGDEPS:=$(shell grep '^diagrams:' $(_DEPS_CACHE) | sed 's/^diagrams://')
# BIBDEPS=$(shell dependencies bibinputs $(BASE).md)

POSTFLAGS=$(shell flags post $(BASE))
PPTXFLAGS=$(shell flags pptx $(BASE))
DOCXFLAGS=$(shell flags docx $(BASE))
SFLAGS=$(shell flags reveal $(BASE))

TALKLISTFILES=$(shell ${FIND} ${TALKSDIR} -type f)
PUBLICATIONLISTFILES=$(shell ${FIND} ${PUBLICATIONSDIR} -type f)
TEACHINGLISTFILES=${PROJECTSDIR}/teaching.yaml
PROJECTLISTFILES=${PROJECTSDIR}/grants.yaml
MEETINGLISTFILES=${PROJECTSDIR}/workshops.yaml
GROUPLISTFILES=$(shell ${FIND} ${GROUPDIR} -type f)  
EXSTUDENTFILES=${DATADIR}/students.yaml
EXRAFILES=${DATADIR}/ras.yaml

# Get all dependencies (extracted from batch call above)
DYNAMIC_DEPS:=$(shell grep '^all:' $(_DEPS_CACHE) | sed 's/^all://')
# Clean up temp file after all extractions are complete
_CLEANUP:=$(shell rm -f $(_DEPS_CACHE))
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
