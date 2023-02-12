# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pymeasurement'
copyright = '2023, Saptak Das'
author = 'Saptak Das'
release = '1.0.6'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_copybutton'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# html_theme_options = {
#     "github_user": "Saptak625",
#     "github_repo": "pymeasurement",
#     "github_button": True,
#     "github_type": "star",
#     "github_count": True,
#     "sidebar_width": "300px",
# }

# html_sidebars = {
#     "**": [
#         "about.html",
#         "navigation.html",
#         "relations.html",
#         "searchbox.html",
#         "donate.html",
#     ]
# }