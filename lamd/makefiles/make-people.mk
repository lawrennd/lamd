talk-people.gpp: ${PEOPLEYAML}
	@if [ -z "${PEOPLEYAML}" ]; then \
		echo "Error: No people YAML file specified. Please specify a 'people' field in either:"; \
		echo "1. Your markdown frontmatter:"; \
		echo "---"; \
		echo "title: Your Title"; \
		echo "people: path/to/people.yaml"; \
		echo "---"; \
		echo ""; \
		echo "2. Or in your _lamd.yml configuration file (preferred):"; \
		echo "people: path/to/people.yaml"; \
		echo ""; \
		echo "Note: _config.yml is deprecated and only supported for backwards compatibility."; \
		exit 1; \
	fi
	mdpeople -i ${PEOPLEYAML} -o $@
