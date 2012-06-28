#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""
Setup script
"""

from distutils.core import setup
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
    )

