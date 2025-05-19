# First, let's create a docs structure
docs_structure = """
lamd/
  ├── docs/
  │   ├── _build/          # Built documentation
  │   ├── _static/         # Static files like images
  │   ├── _templates/      # Custom Sphinx templates
  │   ├── conf.py          # Sphinx configuration
  │   ├── index.rst        # Main documentation entry point
  │   ├── macros/          # Macro documentation
  │   │   ├── index.rst    # Macro documentation entry point
  │   │   ├── overview.md  # Overview of macro system
  │   │   ├── reference.md # Detailed macro reference
  │   │   └── examples.md  # Example patterns and usage
  │   ├── make.bat        # Windows build script
  │   └── Makefile        # Unix build script
  └── README.md           # Main project README
"""

conf_py = """
# Configuration file for Sphinx documentation builder
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'LAMD'
copyright = '2024, Neil D. Lawrence'
author = 'Neil D. Lawrence'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',  # For Markdown support
]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# Theme
html_theme = 'sphinx_rtd_theme'
"""

index_rst = """
Welcome to LAMD Documentation
===========================

LAMD (Lecture And Meeting Documentation) is a macro language for creating academic content
that can be rendered in multiple formats.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   macros/index
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
"""

macros_index_rst = """
LAMD Macro Reference
==================

.. toctree::
   :maxdepth: 2

   overview
   reference
   examples
"""

requirements_txt = """
sphinx
sphinx-rtd-theme
myst-parser
"""

github_workflow = """
name: Build Documentation

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'docs/**'

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        pip install -r docs/requirements.txt
    
    - name: Build documentation
      run: |
        cd docs
        make html
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: docs/_build/html
"""
