# LaMD

<p align="left">
  <a href="https://github.com/lawrennd/lamd/actions/workflows/python-tests.yml"><img alt="Tests Status" src="https://github.com/lawrennd/lamd/workflows/Python%20Tests/badge.svg"></a>
  <a href="https://github.com/lawrennd/lamd/actions/workflows/lint.yml"><img alt="Lint Status" src="https://github.com/lawrennd/lamd/workflows/Lint/badge.svg"></a>
  <a href="https://codecov.io/gh/lawrennd/lamd"><img alt="Codecov" src="https://codecov.io/gh/lawrennd/lamd/branch/main/graph/badge.svg"></a>
  <a href="https://lawrennd.github.io/lamd"><img alt="Documentation Status" src="https://github.com/lawrennd/lamd/workflows/documentation/badge.svg"></a>
</p>

A system for creating academic content that can be rendered in multiple formats (slides, notes, papers) from a single source. LaMD provides a rich set of macros and contexts for handling different content types and output formats.

## Documentation

Full documentation is available at:
- [https://inverseprobability.com/lamd](https://lawrennd.github.io/lamd)

Key sections:
- [Getting Started](https://https://inverseprobability.com/lamd/intro/installation.html)
- [Context Reference](https://inverseprobability.com/lamd/contexts/)
- [Usage Guides](https://inverseprobability.com/lamd/guides/)

## Installation

The system relies on the generic preprocessor, `gpp` ([https://github.com/logological/gpp](https://github.com/logological/gpp)).

On Linux:
```bash
apt-get install gpp
```

On macOS:
```bash
brew install gpp
```

```bash
# Install lamd using pip
pip install lamd

# Or install from source using Poetry
git clone https://github.com/lawrennd/lamd.git
cd lamd
poetry install
```

## Dependencies

LaMD requires:
- Python 3.11 or higher
- gpp preprocessor
- Pandoc (for document conversion)
- Additional Python packages (installed automatically):
  - lynguine
  - python-frontmatter
  - pandas
  - python-liquid

## Configuration

Create a `_lamd.yml` in your project root to configure pandoc flags and other settings:

```yaml
```

## Configuration System

LaMD uses a modular configuration system based on makefiles and markdown frontmatter:

### Flag Files

Configuration is organized into flag files for different document types:
- `make-cv-flags.mk`: Configuration for CV documents
- `make-talk-flags.mk`: Configuration for talk documents
- etc.

These flag files:
1. Extract configuration from markdown frontmatter using `mdfield`
2. Define document-specific settings and paths
3. Are included by the make system as needed

### Configuration Sources

Configuration can come from:
1. Markdown frontmatter (primary source)
2. Flag files (document-type specific)
3. Environment variables (for system-wide settings)

### Example Configuration Flow

For a talk document:
1. The markdown file's frontmatter defines basic settings along with _lamd.yml that contains the defaults.
2. `make-talk-flags.mk` extracts these settings using `mdfield`
3. The make system includes these flags
4. The Python code (`mdpp.py`) respects these settings

## Core Scripts

LaMD provides several utility scripts:

* `maketalk`: Converts talk files from markdown to other formats
* `makecv`: Converts CVs from markdown to other formats
* `flags`: Extracts pandoc flags from `_config.yml`
* `mdfield`: Extracts fields from markdown headers
* `dependencies`: Lists dependencies in markdown files
* `mdpeople`: Generates people macros from YAML definitions
* `mdlist`: Generates lists from YAML definitions

### Managing People Information

The `mdpeople` script provides a powerful way to manage information about people in your documents. It generates macros for displaying profile images and information consistently.

Usage:
```bash
# Generate people macros from YAML file
mdpeople generate -i people.yml -o talk-people.gpp

# List all defined people
mdpeople list -i people.yml

# Check for missing images or invalid URLs
mdpeople verify -i people.yml
```

Example people.yml:
```yaml
- given: Peter
  family: Piper
  image: people/peter-piper.png
  url: https://pepper-pickers.com/
  title: Neil Lawrence

- given: Jack
  family: Spratt
  image: people/jacks.png
  url: https://lowfatyoghurts.com/jackspratt
  title: Jack Spratt
```

Using generated macros:
```markdown
\include{talk-people.gpp}

\section{Team}

Our team includes \neillawrencePicture{15%} and \carlhenrikekPicture{15%}
```

## Features

- Multiple output formats (HTML, PDF, PPTX)
- Context-aware content rendering
- Rich macro system for content reuse
- Media handling (images, videos, diagrams)
- Bibliography management
- People and team pages
- Exercise and assignment support
- Code testing and execution support (`--code test`)

## Example Usage

Create a new talk:
```markdown
# Create talk file
echo "---
title: My Talk
author: Your Name
---

\section{Introduction}

\notes{Detailed notes here}

\slides{
* Bullet points
* For slides
}" > talk.md

# Build different formats
maketalk talk.md --format slides
maketalk talk.md --format notes
```

### Code Testing and Execution

LaMD supports code extraction and testing through the `--code test` option:

```bash
# Extract all code blocks for testing/execution
mdpp input.md --code test --macros-path macros/

# Use \testcode macro for test-specific code
\testcode{
import numpy as np
result = np.mean([1, 2, 3, 4, 5])
assert result == 3.0
print("Test passed!")
}
```

The `--code test` option enables all code inclusion flags (`-DCODE=1`, `-DPLOTCODE=1`, `-DHELPERCODE=1`, `-DDISPLAYCODE=1`, `-DMAGICCODE=1`, `-DTESTCODE=1`) to ensure all code blocks are available for extraction and execution.

## Contributing

- [Source Code](https://github.com/lawrennd/lamd)
- [Issue Tracker](https://github.com/lawrennd/lamd/issues)


## Related Projects

- [Snippets](https://github.com/lawrennd/snippets): Repository of reusable content
- [Talks](https://github.com/lawrennd/talks): Example talks using LaMD

