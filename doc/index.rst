.. MQ² documentation master file, created by
   sphinx-quickstart on Wed Nov 28 11:35:46 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MQ²'s documentation!
===============================

MQ² is a python module and program to analyse output from MapQTL analysis.


Assuming one QTL per linkage group and using the LOD threshold set by the user.
This application extracts all the QTLs detected by MapQTL, using the JoinMap
map file, it finds the closest marker and finally put the number of QTLs found
for each marker on the map.


This approach quickly allows you to find potential QTL hotspot in your
dataset. This is particularly usefull for large QTL analysis on a
large number of traits.


MQ² is licensed under the `GPL v3 or any later version
<http://www.gnu.org/licenses/gpl.txt>`_


Documentation:
--------------

.. toctree::
   :maxdepth: 2

   install
   usage
   output
   contribute

