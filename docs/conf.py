# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# Configuration file for Sphinx documentation builder
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'LaMD'
copyright = '2024, Neil D. Lawrence'
author = 'Neil D. Lawrence'
release = '0.1.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

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
    "field_list",
    "tasklist",
    "attrs_block",    
]

# Source suffix
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']




