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

"""abydos.tests.distance.test_distance_rogers_tanimoto.

This module contains unit tests for abydos.distance.RogersTanimoto
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import RogersTanimoto


class RogersTanimotoTestCases(unittest.TestCase):
    """Test RogersTanimoto functions.

    abydos.distance.RogersTanimoto
    """

    cmp = RogersTanimoto()
    cmp_no_d = RogersTanimoto(alphabet=1)

    def test_rogers_tanimoto_sim(self):
        """Test abydos.distance.RogersTanimoto.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('', 'a'), 0.9949109414758269)
        self.assertEqual(self.cmp.sim('abc', ''), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.9898477157360406)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.9748110831234257)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.9848101266)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.9848101266)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.9848101266)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.9848101266)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.982300885
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3333333333
        )


if __name__ == '__main__':
    unittest.main()
