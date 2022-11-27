invited-talk-list.markdown: ${TALKLISTFILES}
	echo ${TALKLISTFILES}
	mdlist talks $^ -o $@ -s ${TALKSINCE}

publication-list.markdown: ${PUBLICATIONLISTFILES}
	echo ${PUBLICATIONLISTFILES}
	mdlist publications $^ -o $@ -s ${PUBLICATIONSINCE}

meetings-organised-list.markdown: ${MEETINGLISTFILES}
	mdlist meetings $^ -o $@ -s ${MEETINGSINCE}

current-grant-list.markdown: ${PROJECTLISTFILES}
	mdlist grants $^ -o $@

current-teaching-list.markdown: ${TEACHINGLISTFILES}
	mdlist teaching $^ -o $@

previous-teaching-list.markdown: ${TEACHINGLISTFILES}
	mdlist exteaching $^ -o $@

graduated-student-list.markdown: ${EXSTUDENTFILES}
	mdlist exstudents $^ -o $@

former-pdra-list.markdown: ${EXRAFILES}
	mdlist expdras $^ -o $@

previous-grant-list.markdown: ${PROJECTLISTFILES}
	mdlist exgrants $^ -o $@

phd-list.markdown: ${GROUPLISTFILES}
	mdlist students $^ -o $@

ra-list.markdown: ${GROUPLISTFILES}
	mdlist pdras $^ -o $@



lawrence-pubs.yaml: $(shell ${FIND} ${PUBLICATIONSDIR} -type f)
	wget -O $@ http://inverseprobability.com/publications/assets/bib/citeproc.yaml 

