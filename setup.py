#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""
Setup script
"""

from setuptools import setup
from MQ2 import __version__

setup(
    name='MQ2',
    description='MQ² aims at extracting and find QTLs from MapQTL output',
    author='Pierre-Yves Chibon',
    author_email='pingou@pingoured.fr',
    version=__version__,
    license='GPLv3+',
    url='https://github.com/PBR/MQ2/',
    packages=['MQ2', 'MQ2.plugins'],
    install_requires=['straight.plugin', 'xlrd'],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'MQ2 = MQ2.mq2:cli_main'
		]
    },
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
    )

