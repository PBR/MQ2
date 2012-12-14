Output
======

MQ², command line or via its `web interface <https://github.com/PBR/MQ2_Web>`_,
will generate a number of output files for each steps of the procedure,
allowing to follow how the final results have been generated.


.. _qtls.csv:

qtls.csv
~~~~~~~~

The ``qtls.csv`` file list all the QTLs found while parsing the MapQTL output
files. MQ² only extracts the strongest QTL above the LOD threshold per linkage
group for each trait. Each row of this file corresponds to the peak of one of
the QTL found.

When running a MapQTL, one can ask MapQTL to impute putative markers in between
the markers given in the genetic map. As a results, in the `Locus` column of
the ``qtls.csv`` file, some rows might have no values. This means that there
are no marker from the genetic map at this position.

All columns in the ``qtls.csv`` file are directly coming from the MapQTL
output. They correspond to the values that are displayed in the `Result` tab
within MapQTL.


.. _qtls_with_mk.csv:

qtls_with_mk.csv
~~~~~~~~~~~~~~~~

The ``qtls_with_mk.csv`` correspond to the same file as the :ref:`qtls.csv`
with the addition of an extra column `Closest marker` which correspond to the
name of the marker closest to the position of this QTL peak.


.. _map.csv:

map.csv
~~~~~~~

The ``map.csv`` file corresponds to the genetic map provided by the user for
the MapQTL analysis and that MQ² retrieves from the MapQTL output.


map_with_qtl.csv
~~~~~~~~~~~~~~~~

The ``map_with_qtl.csv`` file corresponds to the same file as the
:ref:`map.csv` with the addition of an extra column `# QTLs` corresponding to
the number of QTLs found at this specific marker.

The number of QTLs is compiled from the :ref:`qtls_with_mk.csv` file using the
added column `Closest marker`.


qtls_matrix.csv
~~~~~~~~~~~~~~~

The ``qtls_matrix.csv`` file is a matrix providing for each trait analysed and
for each marker on the genetic map the LOD value found by MapQTL.

An extra column `# QTLs` is added at the end of the file providing the number
traits having a LOD value above the LOD threshold for that specific marker.

This matrix gives the possibility to have an overview of the QTL interval for
each trait.


MapChart.map
~~~~~~~~~~~~

.. versionadded:: 0.2

`MapChart <http://wageningenur.nl/en/show/Mapchart.htm>`_ is a window-specific
(freely available) program to visualize QTLs on a genetic map.

MQ² provides a ``MapChart.map`` output file which can be loaded directly into
MapChart and will allow a more detail visualisation of the QTL intervals on the
genetic map.

More information about MapChart can also be found in:

::

  Voorrips, R.E., 2002. MapChart: Software for the graphical presentation of
  linkage maps and QTLs. The Journal of Heredity 93 (1): 77-78.

