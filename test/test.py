#!/usr/bin/python
#-*- coding: utf-8 -*-

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

 MQ² test script
"""

import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.abspath('../'))

from src import (set_tmp_folder, extract_zip,
    MQ2NoMatrixException, MQ2NoSuchSessionException)
from src.generate_map_from_mapqtl import generate_map_from_mapqtl
from src.parse_mapqtl_file import parse_mapqtl_file
from src.add_marker_to_qtls import add_marker_to_qtls
from src.add_qtl_to_map import add_qtl_to_map

TEST_INPUT_PASSED = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'Demoset1.zip')
TEST_INPUT_FAILED = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'Demoset2.zip')
TEST_INPUT_FAKE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'fake.zip')


def clean_directory():
    """ Remove the 'demo_test' folder is present in the current
    working directory.
    """
    if os.path.exists('demo_test') and os.path.isdir('demo_test'):
        shutil.rmtree('demo_test')
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            os.unlink(filename)


## TODO: check the file exists is good, check that the file has the
## expected content is even better...
class MQ2tests(unittest.TestCase):
    """ MQ² tests. """

    def __init__(self, method_name='runTest'):
        """ Constructor. """
        unittest.TestCase.__init__(self, method_name)

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        clean_directory()

    def tearDown(self):
        """ Clean up the environnment, ran after every tests. """
        clean_directory()

    def test_extract_zip(self):
        """ Test MQ² with correct information """
        mapqtl_folder = set_tmp_folder()

        extract_zip(TEST_INPUT_PASSED, mapqtl_folder)
        self.assertTrue(os.path.exists(mapqtl_folder))

        expected_files = ['Session 2 (IM)_A_trait01.mqo',
            'Session 2 (IM)_A_trait02.mqo']
        found_files = os.listdir(mapqtl_folder)
        found_files.sort()
        self.assertEqual(found_files, expected_files)

        generate_map_from_mapqtl(inputfolder=mapqtl_folder,
                sessionid='2')
        self.assertTrue(os.path.exists('map.csv'))

        parse_mapqtl_file(inputfolder=mapqtl_folder,
                sessionid=2,
                lodthreshold=3,
                qtl_outputfile='qtls.csv')
        self.assertTrue(os.path.exists('qtls.csv'))

        add_marker_to_qtls(qtlfile='qtls.csv',
            mapfile='map.csv',
            outputfile='qtls_with_mk.csv')
        self.assertTrue(os.path.exists('qtls_with_mk.csv'))

        add_qtl_to_map(qtlfile='qtls_with_mk.csv',
            mapfile='map.csv',
            outputfile='map_with_qtl.csv')
        self.assertTrue(os.path.exists('map_with_qtl.csv'))

        shutil.rmtree(mapqtl_folder)
        self.assertFalse(os.path.exists(mapqtl_folder))

    def test_mq2_exception(self):
        """ Test MQ² exceptions """
        mapqtl_folder = set_tmp_folder()
        extract_zip(TEST_INPUT_PASSED, mapqtl_folder)
        self.assertTrue(os.path.exists(mapqtl_folder))

        try:
            generate_map_from_mapqtl(inputfolder=mapqtl_folder,
                sessionid='1')
        except MQ2NoSuchSessionException, err:
            self.assertEqual(str(err),
                'No file corresponds to the session "1"')

        try:
            generate_map_from_mapqtl(inputfolder=mapqtl_folder,
                sessionid=1)
        except MQ2NoSuchSessionException, err:
            self.assertEqual(str(err),
                'No file corresponds to the session "1"')

        try:
            parse_mapqtl_file(inputfolder=mapqtl_folder,
                sessionid='1',
                lodthreshold=3,
                qtl_outputfile='qtls.csv')
        except MQ2NoSuchSessionException, err:
            self.assertEqual(str(err),
                'No file corresponds to the session "1"')

        extract_zip(TEST_INPUT_FAILED, mapqtl_folder)
        self.assertTrue(os.path.exists(mapqtl_folder))

        generate_map_from_mapqtl(inputfolder=mapqtl_folder,
                sessionid=2)
        try:
            parse_mapqtl_file(inputfolder=mapqtl_folder,
                sessionid=2,
                lodthreshold=3,
                qtl_outputfile='qtls.csv')
        except MQ2NoMatrixException, err:
            self.assertTrue(str(err).startswith(
            'The map used in the file'))
            self.assertTrue(str(err).endswith(
            'Session 2 (IM)_A_trait02.mqo" does not correspond to the '\
            'map used in at least one other file.'))

        shutil.rmtree(mapqtl_folder)
        self.assertFalse(os.path.exists(mapqtl_folder))

    def test_mq2_fake_zip(self):
        """ Test MQ² with a fake zip file """
        mapqtl_folder = set_tmp_folder()
        extract_zip(TEST_INPUT_FAKE, mapqtl_folder)
        self.assertTrue(os.path.exists(mapqtl_folder))

        found_files = os.listdir(mapqtl_folder)
        self.assertTrue(found_files == [])

        shutil.rmtree(mapqtl_folder)
        self.assertFalse(os.path.exists(mapqtl_folder))


SUITE = unittest.TestLoader().loadTestsFromTestCase(MQ2tests)
unittest.TextTestRunner(verbosity=2).run(SUITE)
