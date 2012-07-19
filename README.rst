MQ²
===

:Author: Pierre-Yves Chibon <pierre-yves.chibon@wur.nl>, <pingou@pingoured.fr>


A simple python module to process output from MapQTL analysis.

Assuming one QTL per linkage group and using the LOD threshold set by the user.
This application extracts all the QTLs detected by MapQTL, using the JoinMap
map file, it finds the closest marker and finally put the number of QTLs found
for each marker on the map.

This approach quickly allows you to find potential QTL hotspot in your
dataset. This is particularly usefull for large QTL analysis on a
large number of traits.

Get this project:
-----------------
Sources:  https://github.com/PBR/MQ2

Release: http://pypi.python.org/packages/source/M/MQ2/MQ2-0.1.0.tar.gz

Run it on the web at: http://www.plantbreeding.wur.nl/mq2


Dependencies:
-------------
- python (2.5 minimum)


Install the project:
--------------------

There are two ways to install this project:

From the sources

- clone the source

::

 git clone https://github.com/PBR/MQ2.git

- Enter the folder and run the setup.py script

::

 cd MQ2
 sudo python setup.py install

From pypi

- Download and install the project from pypi

::

 easy_install MQ2


Run the project:
----------------

To run the project, simply run the ``MQ2`` script provided.

See ``MQ2 --help`` or ``MQ2 -h`` for the different argument available.


Testing:
--------

This project contains unit-tests allowing you to check if the code
behaves as it should.

To run them, two ways, either::

 nosetests

from the ``MQ2`` folder, or::

 python test.py

within the ``test`` folder


License:
--------

This project is licensed GPLv3+.
