#-*- coding: UTF-8 -*-

"""
 (c) 2011-2013 - Copyright Pierre-Yves Chibon

 Distributed under License GPLv3 or later
 You can find a copy of this license on the website
 http://www.gnu.org/licenses/gpl.html

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 MA 02110-1301, USA.
"""


import datetime
import logging
import os
import tarfile
import tempfile
import zipfile

LOG = logging.getLogger('MQ2')

__version__ = '1.1.0'


def set_tmp_folder():
    """ Create a temporary folder using the current time in which
    the zip can be extracted and which should be destroyed afterward.
    """
    output = "%s" % datetime.datetime.now()
    for char in [' ', ':', '.', '-']:
        output = output.replace(char, '')
    output.strip()
    tmp_folder = os.path.join(tempfile.gettempdir(), output)
    return tmp_folder


def extract_zip(filename, extract_dir):
    """ Extract the sources in a temporary folder.
    :arg filename, name of the zip file containing the data from MapQTL
    which will be extracted
    :arg extract_dir, folder in which to extract the archive.
    """
    LOG.info("Extracting %s in %s " % (filename, extract_dir))
    if not os.path.exists(extract_dir):
        try:
            os.mkdir(extract_dir)
        except IOError as err:  # pragma: no cover
            LOG.info("Could not generate the folder %s" % extract_dir)
            LOG.debug("Error: %s" % err)
            return

    if zipfile.is_zipfile(filename):
        try:
            zfile = zipfile.ZipFile(filename, "r")
            for name in zfile.namelist():
                if os.path.dirname(name):
                    curdir = os.path.join(extract_dir, os.path.dirname(name))
                    if not os.path.exists(curdir):
                        os.mkdir(curdir)
                        continue
                outfile = open(os.path.join(extract_dir, name), 'wb')
                outfile.write(zfile.read(name))
                outfile.flush()
                outfile.close()
            zfile.close()
        except IOError as err:  # pragma: no cover
            LOG.info("Error while extracting the zip archive.")
            LOG.debug("Error: %s" % err)
    else:
        try:  # pragma: no cover  We only have zipfile to test with
            tar = tarfile.open(filename)
            tar.extractall(extract_dir)
            tar.close()
        except tarfile.ReadError as err:  # pragma: no cover
            LOG.info("Error while extracting the tarball.")
            LOG.debug("Error: %s" % err)

    return extract_dir


def get_matrix_dimensions(filename):
    """ Reads in a matrix file (comma separated) and returns the number
    of rows and columns.
    :arg filename, the full path to the file to read.
    """
    stream = None
    try:
        stream = open(filename, 'r')
        length = len(stream.readlines())
        stream.seek(0)
        width = len(stream.readline().split(','))
        return (length, width)
    except IOError as err:  # pragma: no cover
        LOG.info("Something wrong happend while reading the file %s "
                 % filename)
        LOG.debug("ERROR: %s" % err)
    finally:
        if stream:
            stream.close()


def read_input_file(filename, sep='\t', noquote=False):
    """Reads a given inputfile (tab delimited) and returns a matrix
    (list of list).
    arg: filename, the complete path to the inputfile to read
    """
    output = []
    stream = None
    try:
        stream = open(filename, 'r')
        for row in stream:
            row = row.strip()
            if noquote:
                row = row.replace('"', '')
            output.append(row.split(sep))
    except IOError as err:  # pragma: no cover
        LOG.info("Something wrong happend while reading the file %s "
                 % filename)
        LOG.debug("ERROR: %s" % err)
    finally:
        if stream:
            stream.close()
    return output


def write_matrix(outputfile, matrix):
    """ Write down the provided matrix in the specified outputfile.
    :arg outputfile, name of the outputfile in which the QTLs found are
        written.
    :arg matrix, the list of lists of data to write.
    """

    try:
        stream = open(outputfile, 'w')
        for row in matrix:
            if isinstance(row, list) or isinstance(row, tuple):
                row = [str(el).strip() for el in row]
                stream.write(','.join(row) + '\n')
            else:
                stream.write(row + '\n')
    except IOError as err:  # pragma: no cover
        LOG.info('An error occured while writing the file %s'
                 % outputfile)
        LOG.debug("Error: %s" % err)
    finally:
        stream.close()
    LOG.info('Wrote QTLs in file %s' % outputfile)


class MQ2Exception(Exception):
    """ Basic exception class to be used by the pymq2 library. """
    pass


class MQ2NoMatrixException(MQ2Exception):
    """ Exception raised when the qtl_matrix file can not be generated
    because the maps used in the mqo files are inconsistent.
    """
    pass


class MQ2NoSessionException(MQ2Exception):
    """ Exception raised when there are no MapQTL files corresponding to
    the session identifier provided by the user.
    """
    pass


class MQ2NoSuchSessionException(MQ2Exception):
    """ Exception raised when there are no MapQTL files corresponding to
    the session identifier provided by the user.
    """
    pass
