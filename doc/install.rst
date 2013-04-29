Install
=======

Dependencies
~~~~~~~~~~~~

MQ² requires `python 2 <http://www.python.org/download/>`_ (version 2.6 and
above) and is compatible with Python 3.


In addition to python MQ² has the following dependencies:

- `straight.plugin <https://pypi.python.org/pypi/straight.plugin/>`_
- `xlrd <https://pypi.python.org/pypi/xlrd>`_ (only required by the Excel
  plugin, if not present only this plugin will be affected)


Install methods
~~~~~~~~~~~~~~~

Install release
---------------

MQ² releases are uploaded on `pypi <http://pypi.python.org/pypi/>`_ and
you can find them on the `pypi MQ2 page <http://pypi.python.org/pypi/MQ2/>`_.

Having MQ² on pypi allows ``easy_install``. You can therefore install the
latest MQ² release by running:

::

  easy_install MQ2

.. note:: This is the recommanded method for users running Windows.


Install from sources
--------------------

On the `pypi MQ² page <http://pypi.python.org/pypi/MQ2/>`_ you can also
download the latest version of the MQ². Once downloaded, you can extract its
content and install it via the ``setup.py``.

The steps are then:

- Download the latest release from `MQ2 pypi page
  <http://pypi.python.org/pypi/MQ2/>`_

- Extract the files somewhere on your system

- Install MQ² using the command:

  ::

    python setup.py install


Install from git
----------------

To install the development version, you need to have `git
<http://git-scm.com/downloads>`_ installed on your system.

Retrieve the sources from the git using the command:

::

  git clone https://github.com/PBR/MQ2.git

Then you can either
- run MQ² from the cloned repository using:

  ::

    python MQ2/mq2.py --help

- install MQ² on your system via the command

  ::

    python setup.py install


