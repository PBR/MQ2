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
MQ2 main program
"""


import argparse
import logging
import os
import shutil
import sys

from straight.plugin import load

sys.path.insert(0, os.path.join(os.path.dirname(
                os.path.abspath(__file__)), '..'))

from MQ2 import (__version__,
                 set_tmp_folder,
                 extract_zip,
                 MQ2Exception,
                 read_input_file,
                 write_matrix)
from MQ2.plugin_interface import PluginInterface
from MQ2.add_marker_to_qtls import add_marker_to_qtls
from MQ2.add_qtl_to_map import add_qtl_to_map
from MQ2.mapchart import generate_map_chart_file, append_flanking_markers


logging.basicConfig()
LOG = logging.getLogger('MQ2')


def _get_arguments():  # pragma: no cover
    """ Handle the command line arguments given to this program """
    LOG.debug('Parse command line argument')
    parser = argparse.ArgumentParser(
        description='Command line interface for the MQ² program')

    parser.add_argument(
        '-z', '--zipfile', dest='inputzip', default=None,
        help='Zip file containing the input files.')
    parser.add_argument(
        '-d', '--dir', dest='inputdir', default=None,
        help='Path to a local folder containing the input files.')
    parser.add_argument(
        '-f', '--file', dest='inputfile', default=None,
        help='Path to a local input file.')

    parser.add_argument(
        '--lod', default=3,
        help='LOD threshold to use to assess the significance of a LOD \
        value for a QTL.')

    parser.add_argument(
        '--session', default=None,
        help='Session to analyze if required.')

    parser.add_argument(
        '--verbose', action='store_true',
        help="Gives more info about what's going on")
    parser.add_argument(
        '--debug', action='store_true',
        help="Outputs debugging information")
    parser.add_argument(
        '--version', action='version',
        version='MQ² version: %s' % __version__)
    return parser.parse_args()


def cli_main():  # pragma: no cover
    """ Main function when running from CLI. """
    if '--debug' in sys.argv:
        LOG.setLevel(logging.DEBUG)
    elif '--verbose' in sys.argv:
        LOG.setLevel(logging.INFO)

    args = _get_arguments()
    try:
        plugin, folder = get_plugin_and_folder(
            inputzip=args.inputzip,
            inputdir=args.inputdir,
            inputfile=args.inputfile)
        LOG.debug('Plugin: %s -- Folder: %s' % (plugin.name, folder))
        run_mq2(
            plugin, folder, lod_threshold=args.lod, session=args.session)
    except MQ2Exception as err:
        print(err)
        return 1
    return 0


def get_plugin_and_folder(inputzip=None, inputdir=None, inputfile=None):
    """ Main function. """

    if (inputzip and inputdir) \
            or (inputzip and inputfile) \
            or (inputdir and inputfile):
        raise MQ2Exception('You must provide either a zip file or a '
                           'directory or an input file as input.')
    if not inputzip and not inputdir and not inputfile:
        raise MQ2Exception('You must provide either a zip file or a '
                           'directory or an input file as input.')

    # retrieve input: file, directory, zip
    if inputzip:
        tmp_folder = set_tmp_folder()
        extract_zip(inputzip, tmp_folder)
    elif inputfile:
        tmp_folder = inputfile
    else:
        tmp_folder = inputdir

    # retrieve the plugins
    plugins = load('MQ2.plugins', subclasses=PluginInterface)
    LOG.debug('Plugin loaded: %s' % [plugin.name for plugin in plugins])

    # keep only the plugins that will work
    plugins = [plugin for plugin in plugins if plugin.is_applicable()]
    LOG.debug('Plugin applicable: %s' % [plugin.name for plugin in plugins])

    # keep only the plugins that have the file(s) they need
    if inputfile:
        plugins = [plugin for plugin in plugins
                   if plugin.valid_file(tmp_folder)]
    else:
        plugins = [plugin for plugin in plugins
                   if plugin.get_files(tmp_folder)]

    LOG.debug('Plugin w/ valid input: %s' %
              [plugin.name for plugin in plugins])

    if len(plugins) > 1:
        raise MQ2Exception('Your dataset contains valid input for '
                           'several plugins.')
    if len(plugins) == 0:
        raise MQ2Exception('Invalid dataset: your input cannot not be '
                           'processed by any of the current plugins.')
    plugin = plugins[0]
    return (plugin, tmp_folder)


def run_mq2(plugin, folder, lod_threshold=None, session=None,
            outputfolder=None):
    """ Run the plugin. """

    qtls_file = 'qtls.csv'
    matrix_file = 'qtls_matrix.csv'
    map_file = 'map.csv'
    map_qtl_file = 'map_with_qtls.csv'
    qtls_mk_file = 'qtls_with_mk.csv'
    map_chart_file = 'MapChart.map'
    if outputfolder:  # pragma: no cover
        qtls_file = '%s/%s' % (outputfolder, qtls_file)
        qtls_mk_file = '%s/%s' % (outputfolder, qtls_mk_file)
        matrix_file = '%s/%s' % (outputfolder, matrix_file)
        map_file = '%s/%s' % (outputfolder, map_file)
        map_qtl_file = '%s/%s' % (outputfolder, map_qtl_file)
        map_chart_file = '%s/%s' % (outputfolder, map_chart_file)

    LOG.debug('Call the plugin to create the map, qtls and matrix files')
    if folder and os.path.isdir(folder):
        plugin.convert_inputfiles(folder=folder, session=session,
                                  lod_threshold=lod_threshold,
                                  qtls_file=qtls_file,
                                  matrix_file=matrix_file,
                                  map_file=map_file)
    else:
        plugin.convert_inputfiles(inputfile=folder, session=session,
                                  lod_threshold=lod_threshold,
                                  qtls_file=qtls_file,
                                  matrix_file=matrix_file,
                                  map_file=map_file)

    LOG.debug('Add the number of QTLs found on the matrix')
    _append_count_to_matrix(matrix_file, lod_threshold)

    LOG.debug('Append the closest marker to the peak')
    add_marker_to_qtls(qtls_file, map_file, outputfile=qtls_mk_file)

    LOG.debug('Put the number of QTLs found on each marker of the map')
    add_qtl_to_map(qtls_mk_file, map_file, outputfile=map_qtl_file)

    LOG.debug('Generate the mapchart file')
    flanking_markers = generate_map_chart_file(
        matrix_file, lod_threshold, map_chart_file=map_chart_file)

    LOG.debug('Append flanking markers to qtl list')
    flanking_markers = append_flanking_markers(
        qtls_mk_file, flanking_markers)

    if folder and os.path.isdir(folder) and os.path.exists(folder):
        shutil.rmtree(folder)
    return 0


def _append_count_to_matrix(qtl_matrixfile, lod_threshold):
    """ Append an extra column at the end of the matrix file containing
    for each row (marker) the number of QTL found if the marker is known
    ie: Locus != ''

    :arg qtl_matrix, the matrix in which to save the output.
    :arg threshold, threshold used to determine if a given LOD value is
        reflective the presence of a QTL.

    """
    if not os.path.exists(qtl_matrixfile):  # pragma: no cover
        raise MQ2Exception('File not found: "%s"' % qtl_matrixfile)
    matrix = read_input_file(qtl_matrixfile, sep=',')
    tmp = list(matrix[0])
    tmp.append('# QTLs')
    matrix[0] = tmp
    cnt = 1
    while cnt < len(matrix):
        row = list(matrix[cnt])
        nr_qtl = 0
        for cel in row[3:]:
            if cel and float(cel) > float(lod_threshold):
                nr_qtl = nr_qtl + 1
        row.append(str(nr_qtl))
        matrix[cnt] = row
        cnt = cnt + 1
    write_matrix(qtl_matrixfile, matrix)


if __name__ == "__main__":  # pragma: no cover
    cli_main()
