# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../src/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pymeasurement'
copyright = '2023, Saptak Das'
author = 'Saptak Das'
release = '1.0.8'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx_copybutton',
    'sphinxcontrib.exceltable'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# html_sidebars = {
#     "**": [
#         "about.html",
#         "navigation.html",
#         "relations.html",
#         "searchbox.html",
#         "donate.html",
#     ]
# }
# html_sidebars = {
#     "index": ["localtoc.html", "search.html"],
#     "**": ["localtoc.html", "search.html"],
# }
# singlehtml_sidebars = {"index": ["localtoc.html", "search.html"]}