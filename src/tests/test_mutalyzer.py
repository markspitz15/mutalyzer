#!/usr/bin/env python

"""
Tests for the Mutalyzer module.
"""

#import logging; logging.basicConfig()
import re
import os
import random
import unittest
import site
from Bio.Seq import Seq

# Todo: Can this be done in a more elegant way?
os.chdir('../..')
site.addsitedir('src')

from Modules import Config
from Modules import Output
import Mutalyzer


class TestMutalyzer(unittest.TestCase):
    """
    Test the Mutalyzer module.
    """

    def setUp(self):
        """
        Initialize test Mutalyzer module.
        """
        self.config = Config.Config()
        self.output = Output.Output(__file__, self.config.Output)

    def test_roll(self):
        """
        Just a variant where we should roll.
        """
        Mutalyzer.process('NM_003002.2:c.273del', self.config, self.output)
        wroll = self.output.getMessagesWithErrorCode('WROLL')
        self.assertTrue(len(wroll) > 0)

    def test_no_roll(self):
        """
        Just a variant where we should not roll.
        """
        Mutalyzer.process('NM_003002.2:c.274del', self.config, self.output)
        wroll = self.output.getMessagesWithErrorCode('WROLL')
        self.assertTrue(len(wroll) == 0)

    def test_ins_cds_start(self):
        """
        Insertion on CDS start boundary should not be included in CDS.
        """
        Mutalyzer.process('NM_000143.3:c.-1_1insCAT', self.config, self.output)
        self.assertEqual(self.output.getIndexedOutput("newprotein", 0), None)

    def test_ins_cds_start_after(self):
        """
        Insertion after CDS start boundary should be included in CDS.
        """
        Mutalyzer.process('NM_000143.3:c.1_2insCAT', self.config, self.output)
        self.assertEqual(self.output.getIndexedOutput("newprotein", 0), '?')


if __name__ == '__main__':
    # Usage:
    #   ./test_mutalyzer.py -v
    # Or, selecting a specific test:
    #   ./test_mutalyzer.py -v TestMutalyzer.test_ins_cds_start
    unittest.main()