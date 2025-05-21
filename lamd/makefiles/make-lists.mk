invited-talk-list.markdown: ${TALKLISTFILES}
	mdlist talks $^ -o $@ -s ${TALKSINCE}

publication-list.markdown: ${PUBLICATIONLISTFILES}
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


# Legacy approach using wget (commented out):
# lawrence-pubs.yaml: $(shell ${FIND} ${PUBLICATIONSDIR} -type f)
# 	wget -O $@ http://inverseprobability.com/publications/assets/bib/citeproc.yaml 

# New approach using the content distribution system:
lawrence-pubs.yaml: $(shell ${FIND} ${PUBLICATIONSDIR} -type f)
	# Use content distribution system to get citations
	python -c "import sys, os; sys.path.append('..'); from content_distribution import ContentRegistry, ContentDistributor; \
		registry = ContentRegistry(os.path.expanduser('~/.lamd/content_registry.yaml')); \
		distributor = ContentDistributor(registry, os.path.expanduser('~/.lamd/cache')); \
		distributor.download_content('citations'); \
		import shutil; \
		shutil.copy(os.path.join(distributor.get_content_path('citations'), 'citeproc.yaml'), '$@')"

