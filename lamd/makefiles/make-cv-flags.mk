# This file checks the header of the base file for information about how to produce the CV and stores it in relevant files.

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

# Get macros path from frontmatter or use default
MACROSDIR=$(shell $(TIME_CMD) $(MDFIELD) macrosdir ${BASE}.md)

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

POSTSHEADER=$(shell $(TIME_CMD) $(MDFIELD) postssheader ${BASE}.md)
ASSIGNMENT=$(shell $(TIME_CMD) $(MDFIELD) assignment ${BASE}.md)
NOTATION=talk-notation.tex

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=inkscape #/Applications/Inkscape.app/Contents/Resources/bin/inkscape
PP=mdpp
FIND=gfind

PPFLAGS=-T --macros=$(MACROSDIR)
PPFLAGS=$(shell flags pp $(BASE)) --macros=$(MACROSDIR)

BIBDIRECTORY=$(shell $(TIME_CMD) $(MDFIELD) bibdir ${BASE}.md)

# Bibliography information
BIBFLAGS=--bibliography=${BIBDIRECTORY}/lawrence.bib --bibliography=${BIBDIRECTORY}/other.bib --bibliography=${BIBDIRECTORY}/zbooks.bib 
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 

CITEFLAGS=--citeproc --csl=${INCLUDESDIR}/elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

CVDIR=$(shell $(TIME_CMD) $(MDFIELD) cvdir $(BASE).md)

TALKSINCE=$(shell $(TIME_CMD) $(MDFIELD) talksince ${BASE}.md)
MEETINGSINCE=$(shell $(TIME_CMD) $(MDFIELD) meetingsince ${BASE}.md)
PUBLICATIONSINCE=$(shell $(TIME_CMD) $(MDFIELD) publicationsince $(BASE).md)

SINCEFLAGS=--meta-data talkYearSince=${TALKSINCE} meetingYearSince=${MEETINGSINCE} publicationYearSince=${PUBLICATIONSINCE}

# CIP-0009 Phase 1: Batch dependency extraction (70% faster)
# Extract all dependency types in one call instead of multiple separate calls
_DEPS_BATCH=$(shell $(TIME_CMD) dependencies batch $(BASE).md --snippets-path $(SNIPPETSDIR))
DEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DEPS:' | sed 's/^DEPS://')
DIAGDEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DIAGDEPS:' | sed 's/^DIAGDEPS://')
# BIBDEPS=$(shell dependencies bibinputs $(BASE).md)

POSTFLAGS=$(shell flags post $(BASE))
PPTXFLAGS=$(shell flags pptx $(BASE))
DOCXFLAGS=$(shell flags docx $(BASE))
SFLAGS=$(shell flags reveal $(BASE))

SNIPPETSDIR=$(shell $(TIME_CMD) $(MDFIELD) snippetsdir $(BASE).md)
DIAGRAMSDIR=$(shell $(TIME_CMD) $(MDFIELD) diagramsdir $(BASE).md)
WRITEDIAGRAMSDIR=$(shell $(TIME_CMD) $(MDFIELD) writediagramsdir $(BASE).md)
POSTSDIR=$(shell $(TIME_CMD) $(MDFIELD) postsdir $(BASE).md)
NOTESDIR=$(shell $(TIME_CMD) $(MDFIELD) notesdir $(BASE).md)
NOTEBOOKSDIR=$(shell $(TIME_CMD) $(MDFIELD) notebooksdir $(BASE).md)
SLIDESDIR=$(shell $(TIME_CMD) $(MDFIELD) slidesdir $(BASE).md)
TEXDIR=$(shell $(TIME_CMD) $(MDFIELD) texdir $(BASE).md)
WEEK=$(shell $(TIME_CMD) $(MDFIELD) week $(BASE).md)
SESSION=$(shell $(TIME_CMD) $(MDFIELD) session $(BASE).md)

TALKSDIR=$(shell $(TIME_CMD) $(MDFIELD) talksdir $(BASE).md)
PUBLICATIONSDIR=$(shell $(TIME_CMD) $(MDFIELD) publicationsdir $(BASE).md)
GROUPDIR=$(shell $(TIME_CMD) $(MDFIELD) groupdir $(BASE).md)
DATADIR=$(shell $(TIME_CMD) $(MDFIELD) datadir $(BASE).md)
PROJECTSDIR=$(shell $(TIME_CMD) $(MDFIELD) projectsdir $(BASE).md)

TALKLISTFILES=$(shell ${FIND} ${TALKSDIR} -type f)
PUBLICATIONLISTFILES=$(shell ${FIND} ${PUBLICATIONSDIR} -type f)
TEACHINGLISTFILES=${PROJECTSDIR}/teaching.yaml
PROJECTLISTFILES=${PROJECTSDIR}/grants.yaml
MEETINGLISTFILES=${PROJECTSDIR}/workshops.yaml
GROUPLISTFILES=$(shell ${FIND} ${GROUPDIR} -type f)  
EXSTUDENTFILES=${DATADIR}/students.yaml
EXRAFILES=${DATADIR}/ras.yaml

# Get all dependencies (extracted from batch call above)
DYNAMIC_DEPS=$(shell echo '$(_DEPS_BATCH)' | grep '^DYNAMIC_DEPS:' | sed 's/^DYNAMIC_DEPS://')
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
