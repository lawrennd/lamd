# This file checks the header of the base file for information about how to produce the talk and stores it in relevant files.

# Extract the date and the prefix of the produced files.
DATE=$(shell mdfield date ${BASE}.md)

CATEGORIES=$(shell mdfield categories ${BASE}.md)

# Get macros path from frontmatter or use default
MACROS=$(shell mdfield macros ${BASE}.md)
MACROS?=macros

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

SLIDESHEADER=$(shell mdfield slidesheader ${BASE}.md)
POSTSHEADER=$(shell mdfield postssheader ${BASE}.md)
ASSIGNMENT=$(shell mdfield assignment ${BASE}.md)
NOTATION=$(shell mdfield notation ${BASE}.md)

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=/Applications/Inkscape.app/Contents/MacOS/inkscape
PP=mdpp

PPFLAGS=-T --macros=$(MACROS)
PPFLAGS=$(shell flags pp $(BASE)) --macros=$(MACROS)

BIBDIRECTORY=$(shell mdfield bibdir ${BASE}.md)

# Bibliography information not yet automatically extracted
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

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
PEOPLEYAML=$(shell mdfield people $(BASE).md)


DEPS=$(shell dependencies inputs $(BASE).md --snippets-path $(SNIPPETSDIR))
DIAGDEPS=$(shell dependencies diagrams $(BASE).md --snippets-path $(SNIPPETSDIR))
DOCXDEPS=$(shell dependencies docxdiagrams $(BASE).md --snippets-path $(SNIPPETSDIR))
PPTXDEPS=$(shell dependencies docxdiagrams $(BASE).md --snippets-path $(SNIPPETSDIR))
TEXDEPS=$(shell dependencies texdiagrams $(BASE).md --snippets-path $(SNIPPETSDIR))

# Get all dependencies and add "talk-people.gpp" as the first entry to trigger a rebuild if the people file changes
DYNAMIC_DEPS=$(shell dependencies all $(BASE).md --snippets-path $(SNIPPETSDIR))
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
	@if [ -z "$(MACROS)" ]; then \
		echo "Error: 'macros' is not defined in your _lamd.yml configuration file."; \
		echo "Please add a 'macros' entry pointing to your macros directory."; \
		echo "Example:"; \
		echo "macros: macros"; \
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

all: check-snippetsdir check-postsdir check-bibdir check-directories check-macros include_dynamic_deps $(ALL)


