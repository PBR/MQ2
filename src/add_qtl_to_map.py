#-*- coding: UTF-8 -*-

"""
 (c) 2011, 2012 - Copyright Pierre-Yves Chibon

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

import logging
try:
    from MQ2 import read_input_file
except ImportError:
    from src import read_input_file

LOG = logging.getLogger('MQ2')


def write_down_map(outputfile, genetic_map):
    """Write down the genetic map as CSV format into the given outputfile.
    :arg outputfile, the name of the file in which the map will be written.
    :arg genetic_map, the CSV version of the genetic map read.
    """
    try:
        stream = open(outputfile, 'w')
    except IOError, err:  # pragma: no cover
        LOG.info('Could not open the file %s to write in' % outputfile)
        LOG.debug("Error: %s" % err)

    try:
        for entry in genetic_map:
            stream.write(','.join(entry) + "\n")
    except IOError, err:  # pragma: no cover
        LOG.info('An error occured while writing the map to the file %s' \
        % outputfile)
        LOG.debug("Error: %s" % err)
    finally:
        stream.close()
    LOG.info('Wrote genetic map in file %s' % outputfile)


def add_qtl_to_marker(marker, qtls):
    """Add the number of QTLs found for a given marker.
    :arg marker, the marker we are looking for the QTL's.
    :arg qtls, the list of all QTLs found.
    """
    cnt = 0
    for qtl in qtls:
        if qtl[-1] == marker[0]:
            cnt = cnt + 1

    marker.append(str(cnt))
    return marker


def add_qtl_to_map(qtlfile, mapfile, outputfile='map_with_qtl.csv'):
    """Main function.
    This function add the number of QTLs found for each marker in the map.

    :arg qtlfile, the output from MapQTL transformed to a csv file via
    'parse_mapqtl_file' which contains the closest markers.
    :arg mapfile, the genetic map with all the markers.
    :kwarg outputfile, the name of the output file in which the map will
    be written.
    """
    qtl_list = read_input_file(qtlfile, ',')
    map_list = read_input_file(mapfile, ',')
    map_list[0].append('# QTLs')
    markers = []
    markers.append(map_list[0])
    qtl_cnt = 0
    for marker in map_list[1:]:
        markers.append(add_qtl_to_marker(marker, qtl_list[1:]))
        qtl_cnt = qtl_cnt + int(markers[-1][-1])
    LOG.info('- %s markers processed in %s' % (len(markers), mapfile))
    LOG.info('- %s QTLs located in the map: %s' % (qtl_cnt, outputfile))
    write_down_map(outputfile, markers)
