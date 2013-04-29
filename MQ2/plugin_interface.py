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
MQ2 plugin interface
"""


class PluginInterface(object):
    """ The interface that each plugin should extends to support their
    file format and tool.

    """

    name = 'plugin name'
    session_name = 'The name of the session to be displayed on the form'

    @classmethod
    def is_applicable(cls):
        """ Functions used to check whether the plugin can be used or
        not.
        This is the function that would check the import and that should
        make sure the rest of the plugin will run smoothly.

        """
        pass

    @classmethod
    def get_files(cls, folder):
        """ Retrieve the list of files the plugin can work on.
        Find this list based on the files name, files extension or even
        actually by reading in the file.

        :arg folder: the path to the folder containing the files to
            check. This folder may contain sub-folders.

        """
        pass

    @classmethod
    def valid_file(cls, filename):
        """ Check if the provided file is a valid file for this plugin.

        :arg filename: the path to the file to check.

        """
        pass

    @classmethod
    def get_session_identifiers(cls, folder=None, inputfile=None):
        """ Retrieve the list of session identifiers contained in the
        data on the folder or the inputfile.

        :kwarg folder: the path to the folder containing the files to
            check. This folder may contain sub-folders.
        :kwarg inputfile: the path to the input file to use

        """
        pass

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
        pass
