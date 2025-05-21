DOWNLOAD_URL=https://raw.githubusercontent.com/lawrennd/macros/master
MACROS=macros
DEPFILE=makedependency_talk.py
DEPS=$(shell ./$(DEPFILE) $(MACROS))

all: talk-macros.gpp

talk-macros.gpp: dummy

# This section demonstrates the transition from direct wget to the content distribution system.
# Legacy approach using wget (commented out):
# %.gpp:
# 	# Download the file
# 	wget -O $@ $(DOWNLOAD_URL)/gpp/$@
# 	touch dummy
# 	DEPS=$(shell ./$(DEPFILE) $@)
# 	echo $(DEPS)
# 	# Call recursively
# 	$(MAKE) $(DEPS)

# New approach using the content distribution system:
%.gpp:
	# Use content distribution system to get macros
	python -c "import sys; sys.path.append('..'); from content_distribution import ContentRegistry, ContentDistributor; \
		registry = ContentRegistry(os.path.expanduser('~/.lamd/content_registry.yaml')); \
		distributor = ContentDistributor(registry, os.path.expanduser('~/.lamd/cache')); \
		distributor.download_content('macros'); \
		import shutil; \
		shutil.copy(os.path.join(distributor.get_content_path('macros'), 'gpp', '$@'), '$@')"
	touch dummy
	DEPS=$(shell ./$(DEPFILE) $@)
	echo $(DEPS)
	# Call recursively
	$(MAKE) $(DEPS)

dummy:
	touch dummy

clean:
	rm *.gpp
	rm dummy
