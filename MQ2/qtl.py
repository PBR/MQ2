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
MQ2, a QTL object that can be used by the plugin and is used by the
    MapChart code.
"""


class QTL(object):
    """ This object represents the QTL information extracted from the
    qtl matrix and needed for the MapChart output.

    """

    def __init__(self):
        """ Default constructor for the QTL object. """
        self.trait = ''
        self.start_mk = 'NA'
        self.start_position = ''
        self.peak_mk = None
        self.peak_start_position = ''
        self.peak_stop_position = ''
        self.stop_position = ''
        self.stop_mk = 'NA'
        self.peak_lod = 0

    def to_string(self):
        """ Return the string as it should be presented in a MapChart
        input file.

        """
        return '%s   %s %s %s %s' % (
            self.trait, self.start_position, self.peak_start_position,
            self.peak_stop_position, self.stop_position)

    def get_flanking_markers(self):
        """ Return the list of the flanking marker correctly ordered. """
        return [self.start_mk, self.stop_mk]

    def __repr__(self):  # pragma: no cover
        """ String representation of the QTL object. """
        return 'QTL<trait: %s, start:%s, peak:%s - %s, stop:%s>' % (
            self.trait,
            self.start_position, self.peak_start_position,
            self.peak_stop_position, self.stop_position)
