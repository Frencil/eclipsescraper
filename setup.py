from setuptools import setup, find_packages
import sys
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='eclipsescraper',
      version=0.3,
      description="Python module for scraping NASA's eclipse site into usable CZML documents",
      long_description=open('README.md').read(),
      classifiers=[
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        ],
      keywords='GIS JSON CZML Cesium Globe Eclipse NASA',
      author="Christopher Clark (Frencil)",
      author_email='frencils@gmail.com',
      url='https://github.com/Frencil/eclipsescraper',
      license='Apache 2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass = {'test': PyTest},
      install_requires=[
          # -*- Extra requirements: -*-
          "czml>=0.3",
          "geopy>=1.7.1",
          "lxml",
          ],
      )

