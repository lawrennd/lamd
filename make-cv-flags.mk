# This file checks the header of the base file for information about how to produce the talk and stores it in relevant files.

# Extract the date and the prefix of the produced files.
DATE=$(shell mdfield date ${BASE}.md)

CATEGORIES=$(shell mdfield categories ${BASE}.md)

MATHJAX="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG"
REVEALJS="https://inverseprobability.com/talks/slides/reveal.js/"

POSTSHEADER=$(shell mdfield postssheader ${BASE}.md)
ASSIGNMENT=$(shell mdfield assignment ${BASE}.md)
NOTATION=$(shell mdfield notation ${BASE}.md)

PREFIX=$(shell flags prefix ${BASE})

# Local calls for the preprocessor and inkscape
INKSCAPE=inkscape #/Applications/Inkscape.app/Contents/Resources/bin/inkscape
PP=mdpp
FIND=gfind

PPFLAGS=-T 
PPFLAGS=$(shell flags pp $(BASE))

BIBFLAGS=--bibliography=../lawrence.bib --bibliography=../other.bib --bibliography=../zbooks.bib 

CITEFLAGS=--citeproc --csl=../elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

CVDIR=$(shell mdfield cvdir $(BASE).md)


DEPS=$(shell dependencies inputs $(BASE).md)
DIAGDEPS=$(shell dependencies diagrams $(BASE).md)
BIBDEPS=$(shell dependencies bibinputs $(BASE).md)

POSTFLAGS=$(shell flags post $(BASE))
PPTXFLAGS=$(shell flags pptx $(BASE))
DOCXFLAGS=$(shell flags docx $(BASE))
SFLAGS=$(shell flags reveal $(BASE))

TALKSDIR=/Users/neil/lawrennd/talks/_posts
PUBLICATIONSDIR=/Users/neil/lawrennd/publications/_posts
GROUPDIR=/Users/neil/mlatcl/mlatcl.github.io/_people
DATADIR=/Users/neil/lawrennd/data
PROJECTSDIR=${DATADIR}

TALKLISTFILES=$(shell ${FIND} ${TALKSDIR} -type f)
PUBLICATIONLISTFILES=$(shell ${FIND} ${PUBLICATIONSDIR} -type f)
TEACHINGLISTFILES=${PROJECTSDIR}/teaching.yaml
PROJECTLISTFILES=${PROJECTSDIR}/grants.yaml
MEETINGLISTFILES=${PROJECTSDIR}/workshops.yaml
GROUPLISTFILES=$(shell ${FIND} ${GROUPDIR} -type f) ${DATADIR}/students.yaml ${DATADIR}/ras.yaml

ALL=$(shell dependencies all $(BASE).md)
