# LaMD

<p align="left">
  <a href="https://github.com/lawrennd/lamd"><img alt="GitHub Actions status" src="https://github.com/lawrennd/lamd/workflows/code-tests/badge.svg"></a>
  <a href="https://lawrennd.github.io/lamd"><img alt="Documentation Status" src="https://github.com/lawrennd/lamd/workflows/documentation/badge.svg"></a>
</p>

A system for creating academic content that can be rendered in multiple formats (slides, notes, papers) from a single source. LaMD provides a rich set of macros and contexts for handling different content types and output formats.

## Documentation

Full documentation is available at:
- [https://lawrennd.github.io/lamd](https://lawrennd.github.io/lamd)

Key sections:
- [Getting Started](https://lawrennd.github.io/lamd/intro/installation.html)
- [Context Reference](https://lawrennd.github.io/lamd/contexts/)
- [Usage Guides](https://lawrennd.github.io/lamd/guides/)

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

## Core Scripts

LaMD provides several utility scripts:

* `maketalk`: Converts talk files from markdown to other formats
* `makecv`: Converts CVs from markdown to other formats
* `flags`: Extracts pandoc flags from `_config.yml`
* `mdfield`: Extracts fields from markdown headers
* `dependencies`: Lists dependencies in markdown files
* `mdpeople`: Generates people macros from YAML definitions

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
- name: Neil Lawrence
  image: \diagramsDir/people/neil-lawrence.png
  url: https://inverseprobability.com/
  title: Neil Lawrence

- name: Carl Henrik Ek
  image: \diagramsDir/people/carl-henrik-ek.png
  url: https://carlhenrik.com
  title: Carl Henrik Ek
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

## Contributing

- [Source Code](https://github.com/lawrennd/lamd)
- [Issue Tracker](https://github.com/lawrennd/lamd/issues)


## Related Projects

- [Snippets](https://github.com/lawrennd/snippets): Repository of reusable content
- [Talks](https://github.com/lawrennd/talks): Example talks using LaMD
