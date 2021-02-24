# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import os
import unittest

import ansible_collections.equinix.metal.plugins.modules.device as device


class TestIsValidHostname(unittest.TestCase):

    def test_valid_hostname(self):
        self.assertTrue(device.is_valid_hostname("good-hostname"))

    def test_leading_dash(self):
        self.assertFalse(device.is_valid_hostname("-hostname"))

    def test_underscores(self):
        self.assertFalse(device.is_valid_hostname("bad_hostname"))
