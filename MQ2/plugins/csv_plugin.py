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

"""
MQ2 CSV plugin
"""

import os
import re

from MQ2 import MQ2Exception, read_input_file, write_matrix
from MQ2.plugin_interface import PluginInterface


def is_csv_file(inputfile):
    """ Return whether the provided file is a CSV file or not.
    This checks if the first row of the file can be splitted by ',' and
    if the resulting line contains more than 4 columns (Markers, linkage
    group, chromosome, trait).

    """
    try:
        stream = open(inputfile)
        row = stream.readline()
    except (IOError, UnicodeDecodeError):  # pragma: no cover
        return False
    finally:
        stream.close()
    content = row.strip().split(',')
    return inputfile.endswith('.csv') and len(content) >= 4


def get_qtls_from_rqtl_data(matrix, lod_threshold):
    """ Retrieve the list of significants QTLs for the given input
    matrix and using the specified LOD threshold.
    This assumes one QTL per linkage group.

    :arg matrix, the MapQTL file read in memory
    :arg threshold, threshold used to determine if a given LOD value is
        reflective the presence of a QTL.

    """
    t_matrix = list(zip(*matrix))
    qtls = [['Trait', 'Linkage Group', 'Position', 'Exact marker', 'LOD']]
    # row 0: markers
    # row 1: chr
    # row 2: pos
    for row in t_matrix[3:]:
        lgroup = None
        max_lod = None
        peak = None
        cnt = 1
        while cnt < len(row):
            if lgroup is None:
                lgroup = t_matrix[1][cnt]

            if lgroup == t_matrix[1][cnt]:
                if max_lod is None:
                    max_lod = float(row[cnt])
                if float(row[cnt]) > float(max_lod):
                    max_lod = float(row[cnt])
                    peak = cnt
            else:
                if max_lod \
                        and float(max_lod) > float(lod_threshold) \
                        and peak:
                    qtl = [row[0],             # trait
                           t_matrix[1][peak],  # LG
                           t_matrix[2][peak],  # pos
                           t_matrix[0][peak],  # marker
                           max_lod,            # LOD value
                           ]
                    qtls.append(qtl)
                lgroup = None
                max_lod = None
                peak = cnt
            cnt = cnt + 1
    return qtls


def get_map_matrix(inputfile):
    """ Return the matrix representation of the genetic map.

    :arg inputfile: the path to the input file from which to retrieve the
        genetic map.

    """
    matrix = read_input_file(inputfile, sep=',', noquote=True)
    output = [['Locus', 'Group', 'Position']]
    for row in matrix:
        if row[0] and not re.match(r'c\d+\.loc[\d\.]+', row[0]):
            output.append([row[0], row[1], row[2]])
    return output


class CSVPlugin(PluginInterface):
    """ Plugin to extract QTLs from a matrix CSV file.

    """

    name = 'CSV plugin'
    session_name = None

    @classmethod
    def is_applicable(cls):
        """ Functions used to check whether the plugin can be used or
        not.
        The CSV plugin relies on stdlib only, nothing to check

        """
        return True

    @classmethod
    def valid_file(cls, filename):
        """ Check if the provided file is a valid file for this plugin.

        :arg filename: the path to the file to check.

        """
        return is_csv_file(filename)

    @classmethod
    def get_files(cls, folder):
        """ Retrieve the list of files the plugin can work on.
        Find this list based on the files name, files extension or even
        actually by reading in the file.

        :arg folder: the path to the folder containing the files to
            check. This folder may contain sub-folders.

        """
        filelist = []
        if folder is None or not os.path.isdir(folder):
            return filelist
        for root, dirs, files in os.walk(folder):
            for filename in files:
                filename = os.path.join(root, filename)
                if is_csv_file(filename):
                    filelist.append(filename)
        return filelist

    @classmethod
    def convert_inputfiles(cls,
                           folder=None,
                           inputfile=None,
                           session=None,
                           lod_threshold=None,
                           qtls_file='qtls.csv',
                           matrix_file='qtls_matrix.csv',
                           map_file='map.csv'):
        """ Convert the input files present in the given folder or
        inputfile.
        This method creates the matrix representation of the QTLs
        results providing for each marker position the LOD value found
        for each trait as well as a representation of the genetic map
        used in the experiment.
        The genetic map should be cleared of any markers added by the
        QTL mapping software.

        :kwarg folder: the path to the folder containing the files to
            check. This folder may contain sub-folders.
        :kwarg inputfile: the path to the input file to use
        :kwarg session: the session identifier used to identify which
            session to process
        :kwarg lod_threshold: the LOD threshold to apply to determine if
            a QTL is significant or not
        :kwarg qtls_file: a csv file containing the list of all the
            significant QTLs found in the analysis.
            The matrix is of type:
               trait, linkage group, position, Marker, LOD other columns
        :kwarg matrix_file: a csv file containing a matrix representation
            of the QTL data. This matrix is of type:
               marker, linkage group, position, trait1 lod, trait2, lod
        :kwarg map_file: a csv file containing the genetic map used
            in this experiment. The map is of structure:
               marker, linkage group, position

        """
        if folder is None and inputfile is None:
            raise MQ2Exception('You must specify either a folder or an '
                               'input file')

        if folder is not None:  # pragma: no cover
            if not os.path.isdir(folder):
                raise MQ2Exception('The specified folder is actually '
                                   'not a folder')
            else:
                inputfiles = cls.get_files(folder)

        if inputfile is not None:  # pragma: no cover
            if os.path.isdir(inputfile):
                raise MQ2Exception('The specified input file is actually '
                                   'a folder')
            else:
                inputfiles = [inputfile]

        if len(inputfiles) == 0:  # pragma: no cover
            raise MQ2Exception('No files correspond to this plugin')

        if len(inputfiles) > 1:  # pragma: no cover
            raise MQ2Exception(
                'This plugin can only process one file at a time')

        try:
            lod_threshold = float(lod_threshold)
        except ValueError:
            raise MQ2Exception('LOD threshold should be a number')

        inputfile = inputfiles[0]

        # QTL matrix and QTL files
        qtls = []
        matrix = read_input_file(inputfile, sep=',', noquote=True)
        qtls.extend(get_qtls_from_rqtl_data(matrix, lod_threshold))
        # format QTLs and write down the selection
        write_matrix(qtls_file, qtls)

        # Write down the QTL matrix
        write_matrix(matrix_file, matrix)

        # Map matrix
        map_matrix = get_map_matrix(inputfile)
        write_matrix(map_file, map_matrix)
