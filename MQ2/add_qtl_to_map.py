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
MQ2, code to add the number of significant QTLs found for each position
    of the genetic map.
"""

import logging

from MQ2 import read_input_file, write_matrix

LOG = logging.getLogger('MQ2')


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


def add_qtl_to_map(qtlfile, mapfile, outputfile='map_with_qtls.csv'):
    """ This function adds to a genetic map for each marker the number
    of significant QTLs found.

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
    write_matrix(outputfile, markers)
