#!/usr/bin/python
#-*- coding: utf-8 -*-

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

 MQ² test script for the Excel plugin
"""

import os
import shutil
import sys
import unittest

from datetime import date

sys.path.insert(0, os.path.abspath('..'))

import MQ2
import MQ2.mq2 as mq2


TEST_INPUT_PASSED = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'xls', 'rqtl_out.xls.zip')
TEST_INPUT_FAILED = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'xls', 'rqtl_out.xls.invalid.zip')
TEST_INPUT_FAILED2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'xls', 'rqtl_out.xls.invalid2.zip')
TEST_INPUT_FAKE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'invalid', 'fake.zip')

TEST_INPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'xls', 'rqtl_out.xls')

TEST_FAKE_INPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'xls', 'fake.xls')

TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))


def clean_directory():
    """ Remove the 'demo_test' folder is present in the current
    working directory.
    """
    if os.path.exists('demo_test') and os.path.isdir('demo_test'):
        shutil.rmtree('demo_test')
    for filename in os.listdir('.'):
        if filename.endswith(('.map', '.xls', '.xlsx', '.csv')):
            os.unlink(filename)


def read_file(filename):
    """ Reads in a file for a given filename and just return the
    content.
    """
    stream = open(filename)
    data = stream.read()
    stream.close()
    return data


class MQ2MapQTLtests(unittest.TestCase):
    """ MQ² tests for MapQTL input. """

    def __init__(self, method_name='runTest'):
        """ Constructor. """
        unittest.TestCase.__init__(self, method_name)

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        clean_directory()

    def tearDown(self):
        """ Clean up the environnment, ran after every tests. """
        clean_directory()

    def test_get_plugin_and_folder(self):
        """ Test the get_plugin_and_folder function with MapQTL zip
        input.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertTrue(os.path.basename(
            folder).startswith(date.today().strftime('%Y%m%d')))
        self.assertEqual(plugin.name, 'Excel plugin')
        self.assertEqual(plugin.session_name, 'Excel sheet')

    def test_get_plugin_and_folder_wrong_input(self):
        """ Test the get_plugin_and_folder function with an invalid
        zip input.
        """
        self.assertRaises(
            MQ2.MQ2Exception,
            mq2.get_plugin_and_folder,
            inputzip=TEST_INPUT_FAKE)

    def test_run_mq2_no_session(self):
        """ Test the run_mq2 function with MapQTL zip input and without
        session identifier.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertRaises(
            MQ2.MQ2NoSessionException,
            mq2.run_mq2,
            plugin, folder, lod_threshold=3, session=None)

    def test_run_mq2_no_folder(self):
        """ Test the run_mq2 function with MapQTL zip input and without
        folder.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertRaises(
            MQ2.MQ2Exception,
            mq2.run_mq2,
            plugin, folder=None, lod_threshold=3, session=2)

    def test_run_mq2_invalid_lod(self):
        """ Test the run_mq2 function with MapQTL zip input and an
        invalid LOD threshold.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertRaises(
            MQ2.MQ2Exception,
            mq2.run_mq2,
            plugin, folder=folder, lod_threshold='a', session='Sheet1')

    def test_run_mq2_invalid_session(self):
        """ Test the run_mq2 function with MapQTL zip input and the
        wrong session identifier.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertRaises(
            MQ2.MQ2NoSuchSessionException,
            mq2.run_mq2,
            plugin, folder, lod_threshold=3, session='Sheet2')

    def test_run_mq2(self):
        """ Test the run_mq2 function from a zip archive.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        mq2.run_mq2(plugin, folder, lod_threshold=3, session='Sheet1')
        self.assertEqual(read_file('qtls.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'qtls.exp')))
        self.assertEqual(read_file('map.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'map.exp')))
        self.assertEqual(read_file('map_with_qtls.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'map_with_qtls.exp')))
        self.assertEqual(read_file('qtls_with_mk.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'qtls_with_mk.exp')))
        ## Checks disabled
        ## Due to python3 or xlrd on python3 compatibility issue
        ## the number of significant number after the commas differs
        ## which of course breaks the check
        #self.assertEqual(read_file('qtls_matrix.csv'),
                         #read_file(os.path.join(
                            #TEST_FOLDER, 'xls', 'qtls_matrix.exp')))
        #self.assertEqual(read_file('MapChart.map'),
                         #read_file(os.path.join(
                            #TEST_FOLDER, 'xls', 'MapChart.exp')))

    def test_run_mq2_from_file(self):
        """ Test the run_mq2 function from a file.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputfile=TEST_INPUT_FILE)
        mq2.run_mq2(plugin,
                    folder=TEST_INPUT_FILE,
                    lod_threshold=3,
                    session='Sheet1')
        self.assertEqual(read_file('qtls.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'qtls.exp')))
        self.assertEqual(read_file('map.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'map.exp')))
        self.assertEqual(read_file('map_with_qtls.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'map_with_qtls.exp')))
        self.assertEqual(read_file('qtls_with_mk.csv'),
                         read_file(os.path.join(
                            TEST_FOLDER, 'xls', 'qtls_with_mk.exp')))
        ## Checks disabled
        ## Due to python3 or xlrd on python3 compatibility issue
        ## the number of significant number after the commas differs
        ## which of course breaks the check
        #self.assertEqual(read_file('qtls_matrix.csv'),
                         #read_file(os.path.join(
                            #TEST_FOLDER, 'xls', 'qtls_matrix.exp')))
        #self.assertEqual(read_file('MapChart.map'),
                         #read_file(os.path.join(
                            #TEST_FOLDER, 'xls', 'MapChart.exp')))

    def test_plugin_valid_file(self):
        """ Test the valid_file method of the plugin.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertFalse(plugin.valid_file(TEST_INPUT_PASSED))
        self.assertTrue(plugin.valid_file(
            os.path.join(folder,os.listdir(folder)[0])))

        self.assertFalse(plugin.valid_file(
            TEST_FAKE_INPUT_FILE))

    def test_plugin_get_files(self):
        """ Test the get_files method of the plugin.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertEqual(len(plugin.get_files(folder)), 1)
        self.assertTrue(
            plugin.get_files(folder)[0].endswith('/rqtl_out.xls'))
        self.assertEqual(plugin.get_files(None), [])

    def test_plugin_get_session_identifiers_failed(self):
        """ Test the get_session_identifiers method of the plugin.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertRaises(
            MQ2.MQ2Exception,
            plugin.get_session_identifiers,
            folder=os.path.join(TEST_FOLDER, 'fake.xls'),
            inputfile=folder)

    def test_plugin_get_session_identifiers(self):
        """ Test the get_session_identifiers method of the plugin.
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)
        self.assertEqual(len(plugin.get_session_identifiers(folder)), 1)
        self.assertEqual(plugin.get_session_identifiers(folder), ['Sheet1'])
        self.assertEqual(plugin.get_session_identifiers(None), [])

        self.assertEqual(plugin.get_session_identifiers(
            folder=os.path.join(TEST_FOLDER, 'fake.xls')), [])

        self.assertEqual(plugin.get_session_identifiers(
            inputfile=folder), [])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MQ2MapQTLtests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
