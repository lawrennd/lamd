# Generated CV lists.
#
# Discover sources in the recipe, never as Make prerequisites. GNU Make
# treats ":" in a prerequisite as a static-pattern separator, so a talks
# tree with URL-like paths (https:/...) crashes makefile parse. Empty
# TALKSDIR/PUBLICATIONSDIR/GROUPDIR must not make find search ".".
#
# List targets are only built when something depends on them (typically
# a CV \include of publication-list.md and similar). Plain CVs therefore
# never scan talks/publications/group trees.
#
# FIND is set in make-cv-flags.mk; default here for isolated tests.
FIND ?= find

# Print *.md under DIR if DIR is set and is a directory; otherwise print nothing.
define find_md
if [ -n "$(1)" ] && [ -d "$(1)" ]; then $(FIND) "$(1)" -name '*.md' -type f; fi
endef

# Invited talks live in talks/_posts. If that directory exists (even empty),
# do not fall back to scanning the rest of the talks tree or cwd.
define find_talk_md
if [ -n "$(1)" ] && [ -d "$(1)/_posts" ]; then $(FIND) "$(1)/_posts" -name '*.md' -type f; \
elif [ -n "$(1)" ] && [ -d "$(1)" ]; then $(FIND) "$(1)" -name '*.md' -type f; fi
endef

invited-talk-list.markdown:
	@files=`$(call find_talk_md,$(TALKSDIR))`; \
	if [ -z "$$files" ]; then : > $@; else mdlist talks $$files -o $@ -s ${TALKSINCE}; fi

publication-list.markdown:
	@files=`$(call find_md,$(PUBLICATIONSDIR))`; \
	if [ -z "$$files" ]; then : > $@; else mdlist publications $$files -o $@ -s ${PUBLICATIONSINCE}; fi

meetings-organised-list.markdown:
	@if [ -n "$(PROJECTSDIR)" ] && [ -f "$(PROJECTSDIR)/workshops.yaml" ]; then \
		mdlist meetings "$(PROJECTSDIR)/workshops.yaml" -o $@ -s ${MEETINGSINCE}; \
	else : > $@; fi

current-grant-list.markdown:
	@if [ -n "$(PROJECTSDIR)" ] && [ -f "$(PROJECTSDIR)/grants.yaml" ]; then \
		mdlist grants "$(PROJECTSDIR)/grants.yaml" -o $@; \
	else : > $@; fi

current-teaching-list.markdown:
	@if [ -n "$(PROJECTSDIR)" ] && [ -f "$(PROJECTSDIR)/teaching.yaml" ]; then \
		mdlist teaching "$(PROJECTSDIR)/teaching.yaml" -o $@; \
	else : > $@; fi

previous-teaching-list.markdown:
	@if [ -n "$(PROJECTSDIR)" ] && [ -f "$(PROJECTSDIR)/teaching.yaml" ]; then \
		mdlist exteaching "$(PROJECTSDIR)/teaching.yaml" -o $@; \
	else : > $@; fi

graduated-student-list.markdown:
	@if [ -n "$(DATADIR)" ] && [ -f "$(DATADIR)/students.yaml" ]; then \
		mdlist exstudents "$(DATADIR)/students.yaml" -o $@; \
	else : > $@; fi

former-pdra-list.markdown:
	@if [ -n "$(DATADIR)" ] && [ -f "$(DATADIR)/ras.yaml" ]; then \
		mdlist expdras "$(DATADIR)/ras.yaml" -o $@; \
	else : > $@; fi

previous-grant-list.markdown:
	@if [ -n "$(PROJECTSDIR)" ] && [ -f "$(PROJECTSDIR)/grants.yaml" ]; then \
		mdlist exgrants "$(PROJECTSDIR)/grants.yaml" -o $@; \
	else : > $@; fi

phd-list.markdown:
	@files=`$(call find_md,$(GROUPDIR))`; \
	if [ -z "$$files" ]; then : > $@; else mdlist students $$files -o $@; fi

ra-list.markdown:
	@files=`$(call find_md,$(GROUPDIR))`; \
	if [ -z "$$files" ]; then : > $@; else mdlist pdras $$files -o $@; fi


# Legacy approach using wget (commented out):
# lawrence-pubs.yaml: $(shell ${FIND} ${PUBLICATIONSDIR} -type f)
# 	wget -O $@ http://inverseprobability.com/publications/assets/bib/citeproc.yaml

# New approach using the content distribution system:
lawrence-pubs.yaml:
	@if [ -z "$(PUBLICATIONSDIR)" ] || [ ! -d "$(PUBLICATIONSDIR)" ]; then \
		echo "Error: PUBLICATIONSDIR is unset or not a directory."; \
		exit 1; \
	fi
	python -c "import sys, os; sys.path.append('..'); from content_distribution import ContentRegistry, ContentDistributor; \
		registry = ContentRegistry(os.path.expanduser('~/.lamd/content_registry.yaml')); \
		distributor = ContentDistributor(registry, os.path.expanduser('~/.lamd/cache')); \
		distributor.download_content('citations'); \
		import shutil; \
		shutil.copy(os.path.join(distributor.get_content_path('citations'), 'citeproc.yaml'), '$@')"
