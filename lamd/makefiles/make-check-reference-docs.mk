# Fail fast if a resolved docx/pptx reference template is missing.
# Shared by talk and CV flag chains so make-docx.mk can depend on this
# phony target in both pipelines.
.PHONY: check-reference-docs
check-reference-docs:
	@for fmt in docx pptx; do \
		ref=$$(flags $$fmt $(BASE) 2>/dev/null | sed 's/^--reference-doc //'); \
		if [ -n "$$ref" ] && [ ! -f "$$ref" ]; then \
			echo "Error: $$fmt reference template not found: $$ref"; \
			echo "Configure 'dotx' / 'potx' in _lamd.yml with a valid path,"; \
			echo "or use a bare filename shipped with lamd (e.g. custom-reference.potx)."; \
			exit 1; \
		fi; \
	done
