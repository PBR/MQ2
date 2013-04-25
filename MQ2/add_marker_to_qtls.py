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
MQ2, code to add the closest marker to a specified location
    (ie: QTL peak).
"""

import logging

from MQ2 import read_input_file, write_matrix

LOG = logging.getLogger('MQ2')


def add_marker_to_qtl(qtl, map_list):
    """Add the closest marker to the given QTL.

    :arg qtl: a row of the QTL list.
    :arg map_list: the genetic map containing the list of markers.

    """
    closest = ''
    diff = None
    for marker in map_list:
        if qtl[1] == marker[1]:
            tmp_diff = float(qtl[2]) - float(marker[2])
            if diff is None or abs(diff) > abs(tmp_diff):
                diff = tmp_diff
                closest = marker
    if closest != '':
        closest = closest[0]
    return closest


def add_marker_to_qtls(qtlfile, mapfile, outputfile='qtls_with_mk.csv'):
    """This function adds to a list of QTLs, the closest marker to the
    QTL peak.

    :arg qtlfile: a CSV list of all the QTLs found.
        The file should be structured as follow::
            Trait, Linkage group, position, other columns

        The other columns will not matter as long as the first three
        columns are as such.
    :arg mapfile: a CSV representation of the map used for the QTL
        mapping analysis.
        The file should be structured as follow::
            Marker, Linkage group, position
    :kwarg outputfile: the name of the output file in which the list of
        QTLs with their closest marker will be written.

    """
    qtl_list = read_input_file(qtlfile, ',')
    map_list = read_input_file(mapfile, ',')
    if not qtl_list or not map_list:  # pragma: no cover
        return
    qtl_list[0].append('Closest marker')
    qtls = []
    qtls.append(qtl_list[0])
    for qtl in qtl_list[1:]:
        qtl.append(add_marker_to_qtl(qtl, map_list))
        qtls.append(qtl)
    LOG.info('- %s QTLs processed in %s' % (len(qtls), qtlfile))
    write_matrix(outputfile, qtls)
