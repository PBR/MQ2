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

from MQ2 import (MQ2Exception, MQ2NoSessionException,
                 MQ2NoSuchSessionException, MQ2NoMatrixException,
                 read_input_file, write_matrix)
from MQ2.plugin_interface import PluginInterface


def get_qtls_matrix(qtl_matrix, matrix, inputfile):
    """Extract for each position the LOD value obtained and save it in a
    matrix.
    This assumes that the first 4 columns are identical accross all mqo
    files (ie: the Group, Position and Locus are the same). This
    assumption should hold true if the files were generated from the
    same map.

    :arg qtl_matrix, the matrix in which to save the output.
    :arg matrix, the MapQTL file read in memory.
    :arg inputfile, name of the inputfile in which the QTLs have been
        found.

    """
    trait_name = inputfile.split(')_', 1)[1].split('.mqo')[0]
    matrix = list(zip(*matrix))
    if matrix[4][0] != 'LOD':
        raise MQ2Exception(
            'The file "%s" is not supported by MQ2. It may contain an '
            'analysis which does not return LOD values '
            '(such as Kruskal-Wallis or permutation test).' % inputfile)

    if not qtl_matrix:
        qtl_matrix = matrix[:4]
    else:
        if matrix[:4] != qtl_matrix[:4]:
            raise MQ2NoMatrixException(
                'The map used in the file "%s" does not'
                ' correspond to the map used in at least one other file.'
                % inputfile)
    tmp = list(matrix[4])
    tmp[0] = trait_name
    qtl_matrix.append(tmp)
    return qtl_matrix


def get_map_matrix(inputfile):
    """ Return the matrix representation of the genetic map.

    :arg inputfile: the path to the input file from which to retrieve the
        genetic map.

    """
    matrix = read_input_file(inputfile)
    output = []
    for row in matrix:
        if row[3]:
            output.append([row[3], row[1], row[2]])
    return output


def get_qtls_from_mapqtl_data(matrix, threshold, inputfile):
    """Extract the QTLs found by MapQTL reading its file.
    This assume that there is only one QTL per linkage group.

    :arg matrix, the MapQTL file read in memory
    :arg threshold, threshold used to determine if a given LOD value is
        reflective the presence of a QTL.
    :arg inputfile, name of the inputfile in which the QTLs have been
        found

    """
    trait_name = inputfile.split(')_', 1)[1].split('.mqo')[0]
    qtls = []
    qtl = None
    for entry in matrix[1:]:
        if qtl is None:
            qtl = entry
        if qtl[1] != entry[1]:
            if float(qtl[4]) > float(threshold):
                qtl[0] = trait_name
                qtls.append(qtl)
            qtl = entry
        if entry[4] == '':  # pragma: no cover
            entry[4] = 0
        if qtl[4] == '':  # pragma: no cover
            qtl[4] = 0
        if float(entry[4]) > float(qtl[4]):
            qtl = entry

    if float(qtl[4]) > float(threshold):
        qtl[0] = trait_name
        if qtl not in qtls:
            qtls.append(qtl)

    return qtls


class MapQTLPlugin(PluginInterface):
    """ Plugin to extract QTLs from MapQTL output files.

    """

    name = 'MapQTL plugin'
    session_name = 'MapQTL session'

    @classmethod
    def is_applicable(cls):
        """ Functions used to check whether the plugin can be used or
        not.
        The MapQTL plugin relies on stdlib only, nothing to check

        """
        return True

    @classmethod
    def valid_file(cls, filename):
        """ Check if the provided file is a valid file for this plugin.

        :arg filename: the path to the file to check.

        """
        return not os.path.isdir(filename) \
            and os.path.basename(filename).startswith('Session ') \
            and filename.endswith('.mqo')

    @classmethod
    def get_files(cls, folder, session_id=''):
        """ Retrieve the list of files the plugin can work on.
        Find this list based on the files name, files extension or even
        actually by reading in the file.
        If a session identifier is specified it will restrict the list
        of files returned to those with this session identifier in their
        name.

        :arg folder: the path to the folder containing the files to
            check. This folder may contain sub-folders.
        :kwarg session_id: the session identifier of the MapQTL output
            to process.

        """
        filelist = []
        if folder is None or not os.path.isdir(folder):
            return filelist
        if session_id is None:
            session_id = ''
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.startswith('Session %s' % session_id) \
                        and filename.endswith('.mqo'):
                    filename = os.path.join(root, filename)
                    filelist.append(filename)
        return filelist

    @classmethod
    def get_session_identifiers(cls, folder=None, inputfile=None):
        """ Retrieve the list of session identifiers contained in the
        data on the folder.

        :kwarg folder: the path to the folder containing the files to
            check. This folder may contain sub-folders.
        :kwarg inputfile: the path to the input file to use

        """
        sessions = []
        if folder is None or not os.path.isdir(folder):
            return sessions
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.startswith('Session ') \
                        and filename.endswith('.mqo'):
                    session = filename.split()[1]
                    if session not in sessions:
                        sessions.append(session)
        return sessions

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

        sessions = cls.get_session_identifiers(folder)
        if session is None:
            raise MQ2NoSessionException(
                'The MapQTL plugin requires a session identifier to '
                'identify the session to process.'
                'Sessions are: %s' % ','.join(sessions))
        elif str(session) not in sessions:
            raise MQ2NoSuchSessionException(
                'The MapQTL session provided (%s) could not be found in the '
                'dataset. '
                'Sessions are: %s' % (session, ','.join(sessions)))

        if folder is not None:
            if not os.path.isdir(folder):  # pragma: no cover
                raise MQ2Exception('The specified folder is actually '
                                   'not a folder')
            else:
                inputfiles = cls.get_files(folder, session_id=session)

        if inputfile is not None:  # pragma: no cover
            if os.path.isdir(inputfile):
                raise MQ2Exception('The specified input file is actually '
                                   'a folder')
            else:
                inputfiles = [inputfile]

        try:
            lod_threshold = float(lod_threshold)
        except ValueError:
            raise MQ2Exception('LOD threshold should be a number')

        inputfiles.sort()

        # QTL matrix and QTL files
        qtl_matrix = []
        qtls = []
        filename = None
        for filename in inputfiles:
            matrix = read_input_file(filename)
            headers = matrix[0]
            qtl_matrix = get_qtls_matrix(qtl_matrix, matrix, filename)
            qtls.extend(get_qtls_from_mapqtl_data(matrix, lod_threshold,
                        filename))
        # format QTLs and write down the selection
        headers[0] = 'Trait name'
        qtls.insert(0, headers)
        write_matrix(qtls_file, qtls)

        # Write down the QTL matrix
        del(qtl_matrix[0])
        # Reorganize a couple of columns
        qtl_matrix.insert(0, qtl_matrix[2])
        del(qtl_matrix[3])
        # write output
        qtl_matrix = list(zip(*qtl_matrix))
        write_matrix(matrix_file, qtl_matrix)

        # Map matrix
        map_matrix = get_map_matrix(inputfiles[0])
        write_matrix(map_file, map_matrix)
