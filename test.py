#!/usr/bin/python
# -*- coding: utf-8 -*-

import lsemoji as ls

import os
import unittest

class TestLSEmoji(unittest.TestCase):

  def setUp(self):
    self.home = os.getenv('HOME')
    ls.unset(self.home)
    pass

  def tearDown(self):
    pass

  def testLS(self):
    self.assertEqual(ls.emoji(self.home), "🏡")
    pass

  def testSet(self):

    ls.set(self.home,'👍')
    self.assertEqual(ls.emoji(self.home), '👍')

    ls.unset(self.home)
    self.assertEqual(ls.emoji(self.home), '🏡')

if __name__ == '__main__':
  unittest.main()