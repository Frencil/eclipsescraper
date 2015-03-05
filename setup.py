try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Christopher Clark (Frencil)',
    'url': '',
    'download_url': '',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['eclipsescraper'],
    'scripts': [],
    'name': 'eclipsescraper'
}

setup(**config)
