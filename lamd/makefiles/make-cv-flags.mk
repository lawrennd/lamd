# This file checks the header of the base file for information about how to produce the talk and stores it in relevant files.

# Extract the date and the prefix of the produced files.
DATE=$(shell mdfield date ${BASE}.md)

CATEGORIES=$(shell mdfield categories ${BASE}.md)

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

PPFLAGS=-T 
PPFLAGS=$(shell flags pp $(BASE))

BIBFLAGS=--bibliography=../lawrence.bib --bibliography=../other.bib --bibliography=../zbooks.bib 

CITEFLAGS=--citeproc --csl=../elsevier-harvard.csl ${BIBFLAGS}

PDSFLAGS=-s ${CITEFLAGS} --mathjax=${MATHJAX} 

CVDIR=$(shell mdfield cvdir $(BASE).md)

TALKSINCE=$(shell mdfield talksince $(BASE).md)
MEETINGSINCE=$(shell mdfield meetingsince $(BASE).md)
PUBLICATIONSINCE=$(shell mdfield publicationsince $(BASE).md)

SINCEFLAGS=--meta-data talkYearSince=${TALKSINCE} meetingYearSince=${MEETINGSINCE} publicationYearSince=${PUBLICATIONSINCE}

DEPS=$(shell dependencies inputs $(BASE).md)
DIAGDEPS=$(shell dependencies diagrams $(BASE).md)
BIBDEPS=${BIBDIRECTORY}/lawrence.bib ${BIBDIRECTORY}/other.bib ${BIBDIRECTORY}/zbooks.bib 
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

ALL=$(shell dependencies all $(BASE).md)
