# This file checks the header of the base file for information about how to produce the talk and stores it in relevant files.

# Choose mdfield implementation: mdfield-server (fast) or mdfield (compatible)
# Set LAMD_USE_SERVER_CLIENT=1 to use shell client (8x faster)
# Default: mdfield (for backward compatibility)
ifeq ($(LAMD_USE_SERVER_CLIENT),1)
    MDFIELD = $(SCRIPTDIR)/mdfield-server
else
    MDFIELD = mdfield
endif

# TIME_CMD is set by maketalk/makecv when profiling is enabled
# When profiling: TIME_CMD = $(SCRIPTDIR)/profile-command
# When normal: TIME_CMD = (empty)

# Extract the date and the prefix of the produced files.
DATE=$(shell $(TIME_CMD) $(MDFIELD) date ${BASE}.md)

CATEGORIES=$(shell $(TIME_CMD) $(MDFIELD) categories ${BASE}.md)

# Extract the layout
LAYOUT=$(shell $(TIME_CMD) $(MDFIELD) layout ${BASE}.md)

# Get macros path from frontmatter 
MACROSDIR=$(shell $(TIME_CMD) $(MDFIELD) macrosdir ${BASE}.md)

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

SLIDESHEADER=$(shell $(TIME_CMD) $(MDFIELD) slidesheader ${BASE}.md)
POSTSHEADER=$(shell $(TIME_CMD) $(MDFIELD) postssheader ${BASE}.md)
ASSIGNMENT=$(shell $(TIME_CMD) $(MDFIELD) assignment ${BASE}.md)
NOTATION=$(shell $(TIME_CMD) $(MDFIELD) notation ${BASE}.md)

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=/Applications/Inkscape.app/Contents/MacOS/inkscape
PP=mdpp

PPFLAGS=-T
PPFLAGS=$(shell flags pp $(BASE))

BIBDIRECTORY=$(shell $(TIME_CMD) $(MDFIELD) bibdir ${BASE}.md)

# Bibliography information not yet automatically extracted
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

SNIPPETSDIR=$(shell $(TIME_CMD) $(MDFIELD) snippetsdir $(BASE).md)
DIAGRAMSDIR=$(shell $(TIME_CMD) $(MDFIELD) diagramsdir $(BASE).md)
WRITEDIAGRAMSDIR=$(shell $(TIME_CMD) $(MDFIELD) writediagramsdir $(BASE).md)
POSTSDIR=$(shell $(TIME_CMD) $(MDFIELD) postsdir $(BASE).md)
PRACTICALSDIR=$(shell $(TIME_CMD) $(MDFIELD) practicalsdir $(BASE).md)
NOTESDIR=$(shell $(TIME_CMD) $(MDFIELD) notesdir $(BASE).md)
NOTEBOOKSDIR=$(shell $(TIME_CMD) $(MDFIELD) notebooksdir $(BASE).md)
SLIDESDIR=$(shell $(TIME_CMD) $(MDFIELD) slidesdir $(BASE).md)
TEXDIR=$(shell $(TIME_CMD) $(MDFIELD) texdir $(BASE).md)
WEEK=$(shell $(TIME_CMD) $(MDFIELD) week $(BASE).md)
SESSION=$(shell $(TIME_CMD) $(MDFIELD) session $(BASE).md)
PEOPLEYAML=$(shell $(TIME_CMD) $(MDFIELD) people $(BASE).md)

# CIP-0009 Phase 1: Batch dependency extraction (70% faster)
# Extract all dependency types in one call instead of 6 separate calls
# This reduces redundant file I/O from ~28s to ~2-3s
_DEPS_BATCH=$(shell $(TIME_CMD) dependencies batch $(BASE).md --snippets-path $(SNIPPETSDIR))
DEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DEPS:' | sed 's/^DEPS://')
DIAGDEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DIAGDEPS:' | sed 's/^DIAGDEPS://')
DOCXDEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DOCXDEPS:' | sed 's/^DOCXDEPS://')
PPTXDEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^PPTXDEPS:' | sed 's/^PPTXDEPS://')
TEXDEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^TEXDEPS:' | sed 's/^TEXDEPS://')
DYNAMIC_DEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DYNAMIC_DEPS:' | sed 's/^DYNAMIC_DEPS://')

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


