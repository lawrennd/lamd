# Installation and Setup

## Prerequisites

- Python 3.7+
- pandoc
- LaTeX installation (for PDF output)
- reveal.js (for slide output)

## Installation Steps

1. Clone the LAMD repository:
```bash
git clone https://github.com/lawrennd/lamd.git
cd lamd
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install pandoc texlive-full

# macOS
brew install pandoc
brew install --cask mactex
```

4. Configure your environment:
```bash
export LAMD_DIR=/path/to/lamd
```

## Directory Structure

Create your project with this recommended structure:
```
your-project/
  ├── _ml/
  │   └── includes/
  ├── _physics/
  │   └── includes/
  └── lectures/
      ├── lecture1.md
      └── lecture2.md
```

## Configuration

Create a `_config.yml` file:
```yaml
lamd:
  snippets_path: "./"
  diagrams_path: "./diagrams"
  edit_url_base: "https://github.com/username/repo/edit/main"
```

## Testing Installation

Create a test file `test.md`:
```markdown
---
title: Test Document
---

\include{_ml/includes/test-snippet.md}
```

Run the compilation:
```bash
lamd build test.md --format slides
lamd build test.md --format notes
```
