import os
import sys
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'Sankey Interactive'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add the path to the source code for autodoc
sys.path.insert(0, os.path.abspath('../../src'))