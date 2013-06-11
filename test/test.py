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

 MQ² test script
"""

import os
import shutil
import sys
import unittest

from datetime import date

sys.path.insert(0, os.path.abspath('../'))

import MQ2
import MQ2.mq2 as mq2
from MQ2.add_marker_to_qtls import add_marker_to_qtls
from MQ2.add_qtl_to_map import add_qtl_to_map


TEST_INPUT_PASSED = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),'mapqtl', 'Demoset1.zip')
TEST_INPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'csv', 'rqtl_out.csv')
TEST_INPUT_FAKE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),'invalid', 'fake.zip')

TEST_INPUT_FAILED = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),'invalid', 'multi_plugin.zip')

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


class MQ2tests(unittest.TestCase):
    """ MQ² tests. """

    def __init__(self, method_name='runTest'):
        """ Constructor. """
        unittest.TestCase.__init__(self, method_name)
        self.mapqtl_folder = MQ2.set_tmp_folder()

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        clean_directory()
        if os.path.exists(self.mapqtl_folder):
            shutil.rmtree(self.mapqtl_folder)
        self.assertFalse(os.path.exists(self.mapqtl_folder))

    def tearDown(self):
        """ Clean up the environnment, ran after every tests. """
        clean_directory()
        if os.path.exists(self.mapqtl_folder):
            shutil.rmtree(self.mapqtl_folder)
        self.assertFalse(os.path.exists(self.mapqtl_folder))

    def test_extract_zip(self):
        """ Test the extract_zip function. """

        MQ2.extract_zip(TEST_INPUT_PASSED, self.mapqtl_folder)
        self.assertTrue(os.path.exists(self.mapqtl_folder))

        expected_files = ['Session 2 (IM)_A_trait01.mqo',
            'Session 2 (IM)_A_trait02.mqo']
        found_files = os.listdir(self.mapqtl_folder)
        found_files.sort()
        self.assertEqual(found_files, expected_files)

    def test_mq2_fake_zip(self):
        """ Test MQ² with a fake zip file """
        mapqtl_folder = MQ2.set_tmp_folder()
        MQ2.extract_zip(TEST_INPUT_FAKE, self.mapqtl_folder)
        self.assertTrue(os.path.exists(self.mapqtl_folder))

        found_files = os.listdir(self.mapqtl_folder)
        self.assertTrue(found_files == [])

    def test_mq2_get_matrix_dimensions(self):
        """ Test MQ² get_matrix_dimensions function """
        (length, width) = MQ2.get_matrix_dimensions(
            os.path.join(TEST_FOLDER,'mapqtl', 'qtls.exp'))
        self.assertEqual(length, 5)
        self.assertEqual(width, 14)

    def test_mq2_read_input_file(self):
        """ Test MQ² read_input_file function """
        matrix = MQ2.read_input_file(
            os.path.join(TEST_FOLDER, 'mapqtl', 'qtls.exp'), sep=',')
        self.assertEqual(len(matrix), 5)
        self.assertEqual(len(matrix[0]), 14)

    def test_MQ2_write_matrix(self):
        """ Test MQ² write_matrix function """
        data = [[1,2,3], [1,2,3,4], 'test']
        datafile = os.path.join(TEST_FOLDER, 'test_matrix.csv')

        self.assertFalse(os.path.exists(datafile))

        MQ2.write_matrix(datafile, data)

        self.assertTrue(os.path.exists(datafile))
        matrix = MQ2.read_input_file(datafile, sep=',')
        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)
        self.assertEqual(len(matrix[1]), 4)
        self.assertEqual(len(matrix[2]), 1)

        os.unlink(datafile)

        self.assertFalse(os.path.exists(datafile))

    def test_get_plugin_and_folder_too_many_inputs(self):
        """ Test the get_plugin_and_folder function with too many inputs
        """
        self.assertRaises(
            MQ2.MQ2Exception,
            mq2.get_plugin_and_folder,
            inputzip=TEST_INPUT_PASSED,
            inputfile=TEST_INPUT_FILE)

    def test_get_plugin_and_folder_no_input(self):
        """ Test the get_plugin_and_folder function with no input
        """
        self.assertRaises(
            MQ2.MQ2Exception,
            mq2.get_plugin_and_folder)

    def test_get_plugin_and_folder_with_folder(self):
        """ Test the get_plugin_and_folder function with too many inputs
        """
        plugin, folder = mq2.get_plugin_and_folder(
            inputzip=TEST_INPUT_PASSED)

        plugin2, folder2 = mq2.get_plugin_and_folder(
            inputdir=folder)
        self.assertEqual(plugin, plugin2)
        self.assertEqual(folder, folder2)

    def test_get_plugin_and_folder_multiple_files_supported(self):
        """ Test the get_plugin_and_folder function with a dataset
        containing different supported files.
        """
        self.assertRaises(
            MQ2.MQ2Exception,
            mq2.get_plugin_and_folder,
            inputzip=TEST_INPUT_FAILED)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MQ2tests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
