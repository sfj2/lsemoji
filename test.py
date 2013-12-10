#!/usr/bin/python
# -*- coding: utf-8 -*-

import lsemoji as ls

import os
import unittest

class TestLSEmoji(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testLS(self):
    self.assertEqual(ls.emoji(os.getenv('HOME')), "🏡")
    pass

if __name__ == '__main__':
  unittest.main()