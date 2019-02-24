# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.tests.distance.test_distance_kuhns_iv.

This module contains unit tests for abydos.distance.KuhnsIV
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsIV


class KuhnsIVTestCases(unittest.TestCase):
    """Test KuhnsIV functions.

    abydos.distance.KuhnsIV
    """

    cmp = KuhnsIV()
    cmp_no_d = KuhnsIV(alphabet=1)

    def test_kuhns_iv_sim(self):
        """Test abydos.distance.KuhnsIV.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9974489795918368)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.0025510204081632655)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4974489796)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4974489796)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6973214286
        )

    def test_kuhns_iv_dist(self):
        """Test abydos.distance.KuhnsIV.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0025510204081632404)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0025510204081634)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.5025510204)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.5025510204)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.5025510204)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.5025510204)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3026785714
        )


if __name__ == '__main__':
    unittest.main()
