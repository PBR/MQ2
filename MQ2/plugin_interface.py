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


class PluginInterface(object):  # pragma: no cover
    """ The interface that each plugin should extends to support their
    file format and tool.

    Each plugin should be able to detect if it can be run or not
    automatically. In case the plugin cannot be used, it should not
    prevent the other plugins from running.

    Each plugin should be able to detect in a folder (which may contain
    subfolders) if there are files they are compatible with.

    For some plugin, multiple analyzes can be submitted at once and the
    plugin needs to know which one should be analyzed.
    This will be the role of the ``session`` argument.

    """

    name = 'plugin name'
    session_name = 'The name of the session to be displayed on the form'

    @classmethod
    def is_applicable(cls):
        """ Functions used to check whether the plugin can be used or
        not.
        This is the function that would check the import and that should
        make sure the rest of the plugin will run smoothly.

        The method ``is_applicable`` will be called by the program and
        should return a simple boolean telling if the plugin can be run
        or not.
        It is this method that should check that all the potential
        dependencies are met for the plugin to run.

        """
        pass

    @classmethod
    def get_files(cls, folder):
        """ Retrieve the list of files the plugin can work on.
        Find this list based on the files name, files extension or even
        actually by reading in the file.

        The method ``get_files`` will browse the provided path for any
        file in the specified folder or sub-folder that the plugin can
        handle.

        .. note:: ``get_files`` should be able to handle the case where
                  the provided path points to a file rather than a
                  folder, in which case the plugin should return an
                  empty list.

        :arg folder: string of the path to the folder containing the
            files to check. This folder may contain sub-folders.

        """
        pass

    @classmethod
    def valid_file(cls, filename):
        """ Check if the provided file is a valid file for this plugin.

        Since MQ² can also be used on a single file via the command-line,
        the ``valid_file`` will then be used to check if the provided
        file can be handled by the plugin.

        .. note:: ``valid_file`` should be able to handle the case where
                  the provided path points to a director rather than a
                  file, in which case the plugin should return a `False`
                  boolean.

        :arg filename: string of the path to the file to check.

        """
        pass

    @classmethod
    def get_session_identifiers(cls, folder=None, inputfile=None):
        """ Retrieve the list of session identifiers contained in the
        data on the folder or the inputfile.

        The method ``get_session_identifiers`` is used by the
        web-interface to present to the user a list of sessions they can
        choose from and by the command line interface, when the user did
        not specified a session or specified an invalid session.

        The ``get_session_identifiers`` method receive either a folder
        or an inputfile argument (and should raise and
        :class:`~MQ2.MQ2Exception` if both are provided). The method
        extract the session identifiers from this input and return them
        as a list. If both ``folder`` and ``inputfile`` are ``None``, it
        may return an empty list.

        :kwarg folder: string of the path to the folder containing the
            files to check. This folder may contain sub-folders.
        :kwarg inputfile: string of the path to the input file to use

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
        for each trait as well as a list of all the significant QTLs
        found in the results and a representation of the genetic map
        used in the experiment.
        The genetic map should be cleared of any markers added by the
        QTL mapping software.

        :kwarg folder: string of the path to the folder containing the
            files to check. This folder may contain sub-folders.
        :kwarg inputfile: string of the path to the input file to use
        :kwarg session: the session identifier used to identify which
            session to process
        :kwarg lod_threshold: the LOD threshold to apply to determine if
            a QTL is significant or not
        :kwarg qtls_file: a csv file containing the list of all the
            significant QTLs found in the analysis.
            The matrix is of type:
            ``trait, linkage group, position, Marker, LOD other columns``
        :kwarg matrix_file: a csv file containing a matrix representation
            of the QTL data. This matrix is of type:
            ``marker, linkage group, position, trait1 lod, trait2, lod``
        :kwarg map_file: a csv file containing the genetic map used
            in this experiment. The map is of structure:
            ``marker, linkage group, position``

        """
        pass
