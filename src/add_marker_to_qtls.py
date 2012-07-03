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
    from MQ2 import read_input_file, MQ2NoSuchSessionException
except ImportError:
    from src import read_input_file, MQ2NoSuchSessionException

LOG = logging.getLogger('MQ2')


def write_down_qtl_found(outputfile, qtls):
    """ Write down all the QTLs found in the specified inputfile to the
    specified outputfile.
    The name of the trait is extracted from the name of the inputfile, it
    is found between the 'IM)_' and '.mqo' of the filename.

    :arg outputfile: name of the outputfile in which the QTLs found are
        written.
    :arg qtls: the list of QTLs identified in the input file.
    """

    try:
        stream = open(outputfile, 'w')
    except IOError, err:
        LOG.info('Could not open the file %s to write in' % outputfile)
        LOG.debug('ERROR: %s' % err)

    try:
        for qtl in qtls:
            stream.write(','.join(qtl) + '\n')
    except IOError, err:
        LOG.info('An error occured while writing the QTLs to the file %s' \
        % outputfile)
        LOG.debug('ERROR: %s' % err)
    finally:
        stream.close()
    LOG.info('Wrote QTLs in file %s' % outputfile)


def add_marker_to_qtl(qtl, map_list):
    """Add the closest marker to the given QTL.

    :arg qtl: a QTL found by MapQTL.
    :arg map_list: the genetic map containing the list of markers.
    """
    closest = ''
    diff = None
    for marker in map_list:
        if qtl[2] == marker[1]:
            tmp_diff = float(qtl[3]) - float(marker[2])
            if diff is None or abs(diff) > abs(tmp_diff):
                diff = tmp_diff
                closest = marker
    if closest != '':
        closest = closest[0]
    return closest


def add_marker_to_qtls(qtlfile, mapfile, outputfile='qtls_with_mk.csv'):
    """Main function.
    This function transform the map file into a csv file.

    :arg qtlfile: the map file from MapQTL to be transformed to csv.
    :arg mapfile: a CSV representation of the map used during the MapQTL
        analysis.
    :kwarg outputfile: the name of the output file in which the map will
    be written.
    """
    qtl_list = read_input_file(qtlfile, ',')
    map_list = read_input_file(mapfile, ',')
    if not qtl_list or not map_list:
        return
    qtl_list[0].append('Closest marker')
    qtls = []
    qtls.append(qtl_list[0])
    for qtl in qtl_list[1:]:
        qtl.append(add_marker_to_qtl(qtl, map_list))
        qtls.append(qtl)
    LOG.info('- %s QTLs processed in %s' % (len(qtls), qtlfile))
    write_down_qtl_found(outputfile, qtls)
