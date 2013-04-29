.. MQ² documentation master file, created by
   sphinx-quickstart on Wed Nov 28 11:35:46 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MQ²'s documentation!
===============================

A simple python module to process output from QTL mapping tool including
`MapQTL <http://www.kyazma.nl/index.php/mc.MapQTL>`_ and
`R/qtl <http://www.rqtl.org/>`_.


Assuming one QTL per linkage group and using the LOD threshold set by the user.
This application extracts all the QTLs detected by the QTL mapping tool, it
finds the closest marker and finally put the number of QTLs found for each
marker on the genetic map.


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
   data
   usage
   output
   contribute
   plugin
