import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'tebetebe'
copyright = '2019, 1papaya'
author = '1papaya'

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 7,
}

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static']

todo_include_todos = True
