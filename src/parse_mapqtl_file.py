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
import os
try:
    from MQ2 import (read_input_file, MQ2Exception,
        MQ2NoMatrixException, MQ2NoSuchSessionException)
except ImportError:
    from src import (read_input_file, MQ2Exception,
        MQ2NoMatrixException, MQ2NoSuchSessionException)

LOG = logging.getLogger('MQ2')


class QTL(object):
    """ This object represents the QTL information extracted from the
    qtl matrix and needed for the MapChart output.
    """

    def __init__(self):
        """ Default constructor for the QTL object. """
        self.trait = ''
        self.start_position = ''
        self.peak_start_position = ''
        self.peak_stop_position = ''
        self.stop_position = ''
        self.peak_lod = 0

    def to_string(self):
        """ Return the string as it should be presented in a MapChart
        input file.
        """
        return '%s   %s %s %s %s' % (self.trait, self.start_position,
            self.peak_start_position, self.peak_stop_position,
            self.stop_position)

    def __repr__(self): # pragma: no cover
        """ String representation of the QTL object. """
        return 'QTL<trait: %s, start:%s, peak:%s - %s, stop:%s>' % (
            self.trait,
            self.start_position, self.peak_start_position,
            self.peak_stop_position, self.stop_position)


def append_count_to_matrix(qtl_matrix, lod_threshold):
    """ Append an extra column at the end of the matrix file containing
    for each row (marker) the number of QTL found if the marker is known
    ie: Locus != ''
    :arg qtl_matrix, the matrix in which to save the output.
    :arg threshold, threshold used to determine if a given LOD value is
    reflective the presence of a QTL.
    """
    tmp = list(qtl_matrix[0])
    tmp.append('# QTLs')
    qtl_matrix[0] = tmp
    cnt = 1
    while cnt < len(qtl_matrix):
        row = list(qtl_matrix[cnt])
        nr_qtl = 0
        for cel in row[4:]:
            if cel and float(cel) > float(lod_threshold):
                nr_qtl = nr_qtl + 1
        row.append(str(nr_qtl))
        qtl_matrix[cnt] = row
        cnt = cnt + 1
    return qtl_matrix


def _extrac_qtl(peak, block, lod_threshold):
    """ Given a row containing the peak of the QTL and all the rows of
    the linkage group of the said QTL (splitted per trait), determine
    the QTL interval and find the start and stop marker of the said
    interval.
    The interval is a LOD 2 interval when the LOD value of the peak is
    above the LOD Threshold + 2 otherwise, the LOD interval is equal to
    Peak LOD - LOD Threshold.
    The approach is conservative in the way it takes the first and last
    marker within the interval.
    :arg peak, a list containing the row information for the peak marker
    :arg block, a list containing all the rows in the linkage group of
    this QTL, splitted per trait.
    :arg log_threshold, threshold used to determine if a given LOD value
    is reflective the presence of a QTL.
    """
    qtls = []
    if not peak:
        return qtls
    for trait in peak:
        threshold = 2
        # Search QTL start
        cnt = block.index(peak[trait])
        start = block[cnt]
        while cnt > 0:
            if block[cnt][-2] == trait:
                if (float(block[cnt][-1]) - float(threshold)) >= 0:
                    start = block[cnt]
            cnt = cnt - 1

        # Search QTL end
        end = []
        cnt = block.index(peak[trait])
        end = block[cnt]
        while cnt < len(block):
            if block[cnt][-2] == trait:
                if (float(block[cnt][-1]) - float(threshold)) >= 0:
                    end = block[cnt]
            cnt = cnt + 1

        qtl = QTL()
        qtl.trait = trait
        qtl.start_position = start[1]
        qtl.peak_start_position = peak[trait][1]
        qtl.peak_stop_position = peak[trait][1]
        qtl.stop_position = end[1]
        qtls.append(qtl)
    return qtls


def _order_linkage_group(group):
    """ For a given group (ie: a list containing [marker, position])
    order the list according to their position.
    """
    tmp = {}
    for row in group:
        if float(row[1]) in tmp:  # pragma: no cover
            tmp[float(row[1])].append(row[0])
        else:
            tmp[float(row[1])] = [row[0]]
    
    keys = tmp.keys()
    keys.sort()
    output = []
    for key in keys:
        for entry in tmp[key]:
            if not entry:
                continue
            output.append([entry, str(key)])
    return output


def generate_map_chart_file(qtl_matrix, lod_threshold,
    map_chart_file='MapChart.map'):
    """ This function converts our QTL matrix file into a MapChart input
    file.
    :arg qtl_matrix, qtl matrix as generated by the get_qtls_matrix
    function.
    :arg lod_threshold, threshold used to determine if a given LOD value
    is reflective the presence of a QTL.
    :kwarg map_chart_file, name of the output file containing the
    MapChart information.
    """
    tmp_dic = {}
    cnt = 1
    tmp = {}
    block = []
    for row in qtl_matrix[1:]:
        linkgrp = qtl_matrix[cnt - 1][1]
        if cnt == 1:
            linkgrp = qtl_matrix[cnt][1]

        if not linkgrp in tmp_dic:
            tmp_dic[linkgrp] = [[], []]

        infos = row[1:4]
        if qtl_matrix[cnt][1] != linkgrp:
            qtls = _extrac_qtl(tmp, block, lod_threshold)
            tmp_dic[linkgrp][1] = qtls
            linkgrp = qtl_matrix[cnt][1]
            tmp_dic[linkgrp] = [[], []]
            tmp = {}
            block = []

        tmp_dic[linkgrp][0].append([row[3], row[2]])

        colcnt = 4
        for cel in row[4:-1]:
            blockrow = infos[:]
            blockrow.extend([qtl_matrix[0][colcnt], cel])
            block.append(blockrow)
            if cel.strip() != '' and float(cel) >= float(lod_threshold):
                temp = infos[:]
                if not tmp:
                    temp.extend([qtl_matrix[0][colcnt], cel])
                    tmp[qtl_matrix[0][colcnt]] = temp
                elif (qtl_matrix[0][colcnt] in tmp and \
                    float(cel) >= float(tmp[qtl_matrix[0][colcnt]][-1])) or \
                    qtl_matrix[0][colcnt] not in tmp:
                    temp.extend([qtl_matrix[0][colcnt], cel])
                    tmp[qtl_matrix[0][colcnt]] = temp
            colcnt = colcnt + 1
        cnt = cnt + 1

    try:
        stream = open(map_chart_file, 'w')
        keys = tmp_dic.keys()
        ## Remove unknown group, reason:
        # The unlinked markers, if present, are always put in group U by
        # MapQTL. If you don't omit them and there are many (often), then
        # their names take so much space that it is difficult to fit them
        # on the page.
        if 'U' in keys:
            keys.remove('U')
        # Try to convert all the groups to float, which would result in
        # a better sorting. If that fails, fail silently.
        try:
            keys = [int(key) for key in keys]
        except ValueError:
            pass
        keys.sort()
        for key in keys:
            key = str(key)  # Needed since we might have converted them to int
            if tmp_dic[key]:
                if key == 'U':  # pragma: no cover
                    # We removed the key before, we should not be here
                    continue
                stream.write('group %s\n' % key)
                for entry in _order_linkage_group(tmp_dic[key][0]):
                    stream.write('  '.join(entry) + '\n')
                if tmp_dic[key][1]:
                    stream.write('\n')
                    stream.write('qtls\n')
                    for qtl in tmp_dic[key][1]:
                        stream.write('%s \n' % qtl.to_string())
                stream.write('\n')
                stream.write('\n')
    except IOError, err:  # pragma: no cover
        LOG.info('An error occured while writing the map chart map ' \
            'to the file %s' % map_chart_file)
        LOG.debug("Error: %s" % err)
    finally:
        stream.close()
    LOG.info('Wrote MapChart map in file %s' % map_chart_file)



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
    matrix = zip(*matrix)
    if not qtl_matrix:
        qtl_matrix = matrix[:4]
    else:
        if matrix[:4] != qtl_matrix[:4]:
            raise MQ2NoMatrixException(
            'The map used in the file "%s" does not' \
            ' correspond to the map used in at least one other file.'\
            % inputfile)
    tmp = list(matrix[4])
    tmp[0] = trait_name
    qtl_matrix.append(tmp)
    return qtl_matrix


def parse_mapqtl_file(inputfolder, sessionid, lodthreshold=3,
        qtl_outputfile='qtls.csv',
        qtl_matrixfile='qtls_matrix.csv',
        map_chart_file='MapChart.map'):
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
    :kwarg qtl_outputfile, the name of the file in which the list of
    QTLs found in the data will be printed. The string should provide
    the full path to the where file should be written.
    :kwarg qtl_matrixfile, the name of the file in a matrix of markers
    per traits will be printed, given for each marker/trait combination
    the LOD value found. The string should provide the full path to the
    where file should be written.
    :kwarg map_chart_file, name of the output file containing the
    MapChart information.
    """

    filelist = get_files_to_read(inputfolder, sessionid)
    if not filelist:
        raise MQ2NoSuchSessionException(
        'No file corresponds to the session "%s"'\
        % sessionid)
    qtls = []
    qtl_matrix = []
    matrix = read_input_file(filelist[0])
    headers = matrix[0]
    headers.insert(0, 'Trait_name')
    qtls.append(headers)
    write_matrix = True
    msg = None
    filelist.sort()
    filename = None
    for filename in filelist:
        matrix = read_input_file(filename)
        try:
            qtl_matrix = get_qtls_matrix(qtl_matrix, matrix, filename)
        except MQ2NoMatrixException, err:
            msg = err
            write_matrix = False
        qtls.extend(get_qtls_from_mapqtl_data(matrix, lodthreshold, filename))
    LOG.info('- %s QTLs found in %s' % (len(qtls), filename))
    write_down_qtl_found(qtl_outputfile, qtls)
    if write_matrix:
        qtl_matrix = zip(*qtl_matrix)
        qtl_matrix = append_count_to_matrix(qtl_matrix, lodthreshold)
        write_down_qtl_found(qtl_matrixfile, qtl_matrix)
        generate_map_chart_file(qtl_matrix, lodthreshold,
            map_chart_file)
    else:
        raise MQ2NoMatrixException(msg)


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
            stream.write(','.join(qtl) + '\n')
    except IOError, err:  # pragma: no cover
        LOG.info('An error occured while writing the QTLs to the file %s' \
        % outputfile)
        LOG.debug("Error: %s" % err)
    finally:
        stream.close()
    LOG.info('Wrote QTLs in file %s' % outputfile)
