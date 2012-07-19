#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""
Setup script
"""

from setuptools import setup
from src import __version__

setup(
    name='MQ2',
    description='MQ² aims at extracting and find QTLs from MapQTL output',
    author='Pierre-Yves Chibon',
    author_email='pingou@pingoured.fr',
    version=__version__,
    license='GPLv3+',
    url='https://github.com/PBR/MQ2/',
    package_dir={'MQ2': 'src'},
    packages=['MQ2'],
    scripts=["MQ2"],
    test_suite = "test.test.MQ2tests",
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
    )

