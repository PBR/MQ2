#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""
Setup script
"""

from distutils.core import setup
from src import __version__

setup(
    name='pymq2',
    description='MQ² aims at extracting and find QTLs from MapQTL output',
    author='Pierre-Yves Chibon',
    author_email='pingou@pingoured.fr',
    version=__version__,
    license='GPLv3+',
    url='https://github.com/PBR/pymq2/',
    package_dir={'pymq2': 'src'},
    packages=['pymq2'],
    scripts=["pymq2"],
    )
