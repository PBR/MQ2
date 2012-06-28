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
from parse_mapqtl_file import get_files_to_read
try:
    from MQ2 import read_input_file, MQ2NoSuchSessionException
except ImportError:
    from src import read_input_file, MQ2NoSuchSessionException

LOG = logging.getLogger('MQ2')


def write_down_map(outputfile, genetic_map):
    """Write down the genetic map as CSV format into the given outputfile.
    :arg outputfile, the name of the file in which the map will be written.
    :arg genetic_map, the CSV version of the genetic map read.
    """
    try:
        stream = open(outputfile, 'w')
    except IOError, err:
        LOG.info('Could not open the file %s to write in' % outputfile)
        LOG.debug("Error: %s" % err)

    try:
        #stream.write("Marker, Linkage group, Position\n")
        for entry in genetic_map:
            stream.write(','.join(entry) + "\n")
    except IOError, err:
        LOG.info('An error occured while writing the map to the file %s' \
            % outputfile)
        LOG.debug("Error: %s" % err)
    finally:
        stream.close()
    LOG.info('Wrote genetic map in file %s' % outputfile)


def generate_map_from_mapqtl(inputfolder, sessionid,
    outputfile='map.csv'):
    """Main function.
    This function transform the map file into a csv file.

    :arg inputfolder, the path to the folder to look into for the data
    file.
    :arg sessionid, the session ID from MapQTL containing the data, this
    is used to identy which files should be read.
    :kwarg outputfile, the name of the output file in which the map will
    be written.
    """

    filelist = get_files_to_read(inputfolder, sessionid)
    if not filelist:
        raise MQ2NoSuchSessionException(
        'No file corresponds to the session "%s"'\
        % sessionid)
    filename = filelist[0]
    matrix = read_input_file(filename)
    output = []
    for row in matrix:
        if row[3]:
            output.append([row[3], row[1], row[2]])
    LOG.info('- %s markers found in the map of %s' % (len(output),
        filename))
    write_down_map(outputfile, output)
    
