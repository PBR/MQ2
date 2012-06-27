#-*- coding: UTF-8 -*-

"""
 (c) Copyright Pierre-Yves Chibon -- 2011, 2012

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

import datetime
import logging
import os
import shutil

try:
    from pymq2 import read_input_file, MQ2Exception
except ImportError:
    from src import read_input_file, MQ2Exception

log = logging.getLogger('pymq2')


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
                qtl.insert(0, trait_name)
                qtls.append(qtl)
            qtl = None
            continue
        if entry[4] == '':
            entry[4] = 0
        if qtl[4] == '':
            qtl[4] = 0
        if float(entry[4]) > float(qtl[4]):
            qtl = entry

    if float(qtl[4]) > float(threshold):
        qtl.insert(0, trait_name)
        if qtl not in qtls:
            qtls.append(qtl)

    return qtls


def get_files_to_read(folder, sessionid):
    """ Reads a given folder and return all the files from MapQTL which
    are from the specified session and are of interest for us.
    So it looks for "Session <sessionid> (IM)_<exp>_<metabolite>.mqo" in
    all the files of the folder.
    :arg folder, path to the folder containing the data
    :arg sessionid, session given in the file name and present in the file
    name
    """
    filelist = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.startswith('Session %s' % sessionid) \
                and filename.endswith('.mqo'):
                filename = os.path.join(root, filename)
                filelist.append(filename)
    return filelist


def write_down_qtl_found(outputfile, qtls):
    """ Write down all the QTLs found in the specified inputfile to the
    specified outputfile.
    The name of the trait is extracted from the name of the inputfile, it
    is found between the 'IM)_' and '.mqo' of the filename.
    :arg outputfile, name of the outputfile in which the QTLs found are
    written.
    :arg qtls, the list of QTLs identified in the input file.
    """

    try:
        stream = open(outputfile, 'w')
        for qtl in qtls:
            stream.write('\t'.join(qtl) + '\n')
    except Exception, err:
        log.info('An error occured while writing the QTLs to the file %s' \
        % outputfile)
        log.debug("Error: %s" % err)
    finally:
        stream.close()
    log.info('Wrote QTLs in file %s' % outputfile)


def parse_mapqtl_file(inputfolder, sessionid, lodthreshold=3,
        outputfolder='.', outputfile='qtls.csv'):
    """Main function.
    This function finds all the file fitting the pattern in the given
    folder, then these files are read and for each a list of QTLs is
    retrieved if their LOD value is above the lod threshold provided.

    :arg inputfolder, the path to the folder to look into for the data
    file.
    :arg sessionid, the session ID from MapQTL containing the data, this
    is used to identy which files should be read.
    :kwarg lodthreshold, the LOD threshold from which we decide if we
    have a QTL.
    :kwarg outputfolder, the name of the folder in whici to write down
    the output files.
    :kwarg outputfile, the name of the file in which the QTLs found in
    the data will be printed.
    """

    filelist = get_files_to_read(inputfolder, sessionid)
    if not filelist:
        raise MQ2Exception('No file corresponds to the session "%s"\
        ' % sessionid)
    qtls = []
    matrix = read_input_file(filelist[0])
    headers = matrix[0]
    headers.insert(0, 'Trait_name')
    qtls.append(headers)
    for filename in filelist:
        matrix = read_input_file(filename)
        qtls.extend(get_qtls_from_mapqtl_data(matrix, lodthreshold, filename))
    log.info('- %s QTLs found in %s' % (len(qtls), filename))
    write_down_qtl_found(os.path.join(outputfolder, outputfile), qtls)
