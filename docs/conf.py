# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import shutil
import sys
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../src"))
shutil.copy("../README.md", "README.md")
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'reldplayer'
copyright = '2024, ZackaryW'
author = 'ZackaryW'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
]

autodoc_mock_imports = [
    "screeninfo",
    "pygetwindow",
    "pyautogui",
    "pyscreeze",
    "pywin32",
    "PIL",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'
locale_dirs = ['locales/']
gettext_compact = False
# This part is for ReadTheDocs to build the docs in different languages
if os.getenv('READTHEDOCS') == 'True':
    language = os.getenv('READTHEDOCS_LANGUAGE', 'en')

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

def setup(app):
    app.add_css_file('custom.css')