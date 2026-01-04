# This file checks the header of the base file for information about how to produce the talk and stores it in relevant files.

# TIME_CMD is set by maketalk/makecv when profiling is enabled
# When profiling: TIME_CMD = $(SCRIPTDIR)/profile-command
# When normal: TIME_CMD = (empty)

# Extract all fields in one call instead of 21 separate calls
# This reduces redundant file I/O and Python startup overhead from ~6s to ~0.5s
# Write batch output to temp file to avoid Make variable issues with multiline content
# NOTE: Always use Python mdfield for batch (mdfield-server shell script doesn't support batch)
_FIELDS_CACHE:=$(shell mktemp)
_FIELDS_EXTRACTED:=$(shell $(TIME_CMD) mdfield batch $(BASE).md --fields date categories layout macrosdir slidesheader postssheader assignment notation bibdir snippetsdir diagramsdir writediagramsdir postsdir practicalsdir notesdir notebooksdir slidesdir texdir week session people > $(_FIELDS_CACHE))

# Parse individual fields from batch output
DATE:=$(shell grep '^date:' $(_FIELDS_CACHE) | sed 's/^date://')
CATEGORIES:=$(shell grep '^categories:' $(_FIELDS_CACHE) | sed 's/^categories://')
LAYOUT:=$(shell grep '^layout:' $(_FIELDS_CACHE) | sed 's/^layout://')
MACROSDIR:=$(shell grep '^macrosdir:' $(_FIELDS_CACHE) | sed 's/^macrosdir://')
SLIDESHEADER:=$(shell grep '^slidesheader:' $(_FIELDS_CACHE) | sed 's/^slidesheader://')
POSTSHEADER:=$(shell grep '^postssheader:' $(_FIELDS_CACHE) | sed 's/^postssheader://')
ASSIGNMENT:=$(shell grep '^assignment:' $(_FIELDS_CACHE) | sed 's/^assignment://')
NOTATION:=$(shell grep '^notation:' $(_FIELDS_CACHE) | sed 's/^notation://')
BIBDIRECTORY:=$(shell grep '^bibdir:' $(_FIELDS_CACHE) | sed 's/^bibdir://')
SNIPPETSDIR:=$(shell grep '^snippetsdir:' $(_FIELDS_CACHE) | sed 's/^snippetsdir://')
DIAGRAMSDIR:=$(shell grep '^diagramsdir:' $(_FIELDS_CACHE) | sed 's/^diagramsdir://')
WRITEDIAGRAMSDIR:=$(shell grep '^writediagramsdir:' $(_FIELDS_CACHE) | sed 's/^writediagramsdir://')
POSTSDIR:=$(shell grep '^postsdir:' $(_FIELDS_CACHE) | sed 's/^postsdir://')
PRACTICALSDIR:=$(shell grep '^practicalsdir:' $(_FIELDS_CACHE) | sed 's/^practicalsdir://')
NOTESDIR:=$(shell grep '^notesdir:' $(_FIELDS_CACHE) | sed 's/^notesdir://')
NOTEBOOKSDIR:=$(shell grep '^notebooksdir:' $(_FIELDS_CACHE) | sed 's/^notebooksdir://')
SLIDESDIR:=$(shell grep '^slidesdir:' $(_FIELDS_CACHE) | sed 's/^slidesdir://')
TEXDIR:=$(shell grep '^texdir:' $(_FIELDS_CACHE) | sed 's/^texdir://')
WEEK:=$(shell grep '^week:' $(_FIELDS_CACHE) | sed 's/^week://')
SESSION:=$(shell grep '^session:' $(_FIELDS_CACHE) | sed 's/^session://')
PEOPLEYAML:=$(shell grep '^people:' $(_FIELDS_CACHE) | sed 's/^people://')

# Clean up temp file immediately after extraction
_FIELDS_CLEANUP:=$(shell rm -f $(_FIELDS_CACHE))

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=/Applications/Inkscape.app/Contents/MacOS/inkscape
PP=mdpp

PPFLAGS=-T
PPFLAGS=$(shell flags pp $(BASE))

# Bibliography information not yet automatically extracted
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX}


# Extract all dependency types in one call instead of 6 separate calls
# This reduces redundant file I/O from ~28s to ~2-3s
# Write batch output to temp file to avoid Make variable issues with multiline content
_DEPS_CACHE:=$(shell mktemp)
# Only pass --snippets-path if SNIPPETSDIR is defined (use shell conditional)
_DEPS_EXTRACTED:=$(shell if [ -n "$(SNIPPETSDIR)" ]; then $(TIME_CMD) dependencies batch $(BASE).md --snippets-path $(SNIPPETSDIR) > $(_DEPS_CACHE); else $(TIME_CMD) dependencies batch $(BASE).md > $(_DEPS_CACHE); fi)
DEPS:=$(shell grep '^inputs:' $(_DEPS_CACHE) | sed 's/^inputs://')
DIAGDEPS:=$(shell grep '^diagrams:' $(_DEPS_CACHE) | sed 's/^diagrams://')
DOCXDEPS:=$(shell grep '^docxdiagrams:' $(_DEPS_CACHE) | sed 's/^docxdiagrams://')
PPTXDEPS:=$(shell grep '^pptxdiagrams:' $(_DEPS_CACHE) | sed 's/^pptxdiagrams://')
TEXDEPS:=$(shell grep '^texdiagrams:' $(_DEPS_CACHE) | sed 's/^texdiagrams://')
DYNAMIC_DEPS:=$(shell grep '^all:' $(_DEPS_CACHE) | sed 's/^all://')
# Clean up temp file immediately after extraction
_CLEANUP:=$(shell rm -f $(_DEPS_CACHE))

# Add "talk-people.gpp" as the first entry to trigger a rebuild if the people file changes
ALL := talk-people.gpp $(DYNAMIC_DEPS)

# After checks, show what dynamic dependencies are included
include_dynamic_deps:
	@if [ -n "$(DYNAMIC_DEPS)" ]; then \
		echo "Including dynamic dependencies: $(DYNAMIC_DEPS)"; \
	fi

POSTFLAGS=$(shell flags post $(BASE))
PPTXFLAGS=$(shell flags pptx $(BASE)) --resource-path .:$(INCLUDESDIR):$(SLIDESDIR)
DOCXFLAGS=$(shell flags docx $(BASE)) --resource-path .:$(INCLUDESDIR):$(SLIDESDIR)
SLIDEFLAGS=$(shell flags reveal $(BASE))

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

.PHONY: check-practicalsdir
check-practicalsdir:
	@if [ "$(LAYOUT)" = "practical" ] && [ -z "$(PRACTICALSDIR)" ]; then \
		echo "Error: 'practicalsdir' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'practicalsdir' entry pointing to your practicals directory."; \
		echo "Example:"; \
		echo "practicalsdir: ../_practicals"; \
		exit 1; \
	fi

.PHONY: check-bibdir
check-bibdir:
	@echo "Checking for bibliography files...";
	@if [ ! -f "${BIBDIRECTORY}/lawrence.bib" ] || [ ! -f "${BIBDIRECTORY}/other.bib" ] || [ ! -f "${BIBDIRECTORY}/zbooks.bib" ]; then \
		echo "Error: Required bibliography files are missing."; \
		echo "Please ensure the following files exist:"; \
		echo "  - ${BIBDIRECTORY}/lawrence.bib"; \
		echo "  - ${BIBDIRECTORY}/other.bib"; \
		echo "  - ${BIBDIRECTORY}/zbooks.bib"; \
		echo "You may need to add a 'bibdir' entry to your _lamd.yml file."; \
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
		echo "macrosdir: $$HOME/lawrennd/lamd/lamd/macros"; \
		exit 1; \
	fi

# Check header for which formats to create in notes and slides.
# Create PDF of reveal slides with something like decktape https://github.com/astefanutti/decktape

OUT=$(PREFIX)$(BASE)

.PHONY: check-directories
check-directories:
	@echo "Checking required directories...";
	@if [ ! -d "$(SNIPPETSDIR)" ]; then \
		echo "Error: Snippets directory '$(SNIPPETSDIR)' does not exist."; \
		echo "Please ensure the 'snippetsdir' entry in your _lamd.yml points to a valid directory."; \
		exit 1; \
	fi
	@if [ ! -d "$(BIBDIRECTORY)" ]; then \
		echo "Error: Bibliography directory '$(BIBDIRECTORY)' does not exist."; \
		echo "Please ensure the 'bibdir' entry in your _lamd.yml points to a valid directory."; \
		exit 1; \
	fi

all: check-snippetsdir check-postsdir check-practicalsdir check-bibdir check-directories check-macros include_dynamic_deps $(ALL)


