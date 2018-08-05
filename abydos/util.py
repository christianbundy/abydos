# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.util.

The util module defines various utility functions for other modules within
Abydos, including:

    - prod -- computes the product of a collection of numbers (akin to sum)
    - jitter -- adds small random noise to each member of a list of numbers
        (ported from R's jitter function)
"""

from __future__ import division, unicode_literals

import math
import random
from operator import mul

import numpy as np

from six import integer_types
from six.moves import range, reduce

numeric_types = integer_types + (complex, float)

_NAN = float('-nan')


def prod(nums):
    """Return the product of nums.

    The product is Π(nums).

    Cf. https://en.wikipedia.org/wiki/Product_(mathematics)

    :param nums: a collection (list, tuple, set, etc.) of numbers
    :returns: the product of a nums

    >>> prod([1,1,1,1])
    1
    >>> prod((2,4,8))
    64
    >>> prod({1,2,3,4})
    24
    >>> prod(2**i for i in range(5))
    1024
    """
    return reduce(mul, nums, 1)


def jitter(nums, factor=1, amount=_NAN, min_val=None, max_val=None,
           rfunc='normal'):
    """Jitter the values in nums.

    Adapted from R documentation, as this is ported directly from the R code:

    The result, say r, is r = x + np.random.uniform(-a, a) where n = len(x)
    and a is the amount argument (if specified).

    Let z = max(x) - min(x) (assuming the usual case). The amount a to be added
    is either provided as positive argument amount or otherwise computed from
    z, as follows:

    If amount == 0, we set a = factor * z/50 (same as S).

    If amount is None (default), we set a = factor * d/5 where d is the
    smallest difference between adjacent unique x values.

    Based on:
    http://svn.r-project.org/R/trunk/src/library/base/R/jitter.R

    :param x:  numeric collection to which jitter should be added
    :param factor:  numeric
    :param amount:  numeric; if positive, used as amount (see below),
        otherwise, if = 0 the default is factor * z/50.
        Default (NULL): factor * d/5 where d is about the smallest difference
        between x values.
    :param min_val: the minimum permitted value in the returned list
    :param max_val: the maximum permitted value in the returned list
    :param rand: a string or function to indicate the random distribution used:
        'normal' (default), 'uniform' (standard in the R version),
        or 'laplace' (requires Numpy)
        If a function is supplied, it should take one argument (the value
        passed as amount).
    :returns: a list of numbers with random noise added, according to the R
        jitter function

    >>> from random import seed
    >>> seed(0)
    >>> jitter(5)
    4.981613177890674
    >>> jitter([5])
    [5.003250412907758]
    >>> jitter([0, 0, 0])
    [0.013976553865079613, -0.0019273569003055062, 0.028270155800962433]
    >>> jitter([i**2 for i in range(3)])
    [-0.3065271742181766, 1.0541873299537723, 3.758893123139162]
    >>> jitter([i**2 for i in range(3)], min_val=0)
    [0.046097833594303306, 0.9419551458754979, 3.9414353766272496]
    """
    if isinstance(nums, numeric_types):
        return jitter([nums])[0]
    if not nums:
        return []
    if sum(isinstance(i, numeric_types) for i in nums) != len(nums):
        raise AttributeError('All members of nums must be numeric.')

    rng = (min(nums), max(nums))
    diff = rng[1]-rng[0]
    if diff == 0:
        diff = abs(rng[0])
    if diff == 0:
        diff = 1

    if min_val is None:
        min_val = rng[0]-diff
    elif rng[0] < min_val:
        raise AttributeError('Minimum of nums is less than min_val.')

    if max_val is None:
        max_val = rng[1]+diff
    elif rng[1] > max_val:
        raise AttributeError('Maximum of nums is greater than max_val.')

    if math.isnan(amount):
        ndigits = int(3 - math.floor(math.log10(diff)))
        snums = sorted({round(i, ndigits) for i in nums})
        if len(snums) == 1:
            if snums[0] != 0:
                scaler = snums[0]/10
            else:
                scaler = diff/10
        else:
            scaler = min(j - snums[i - 1] for i, j in enumerate(snums)
                         if i > 0)
        amount = factor/5 * abs(scaler)
    elif amount == 0:
        amount = factor * (diff/50)

    amount = abs(amount)

    def _rand_uniform():
        """Generate a random number from the uniform distribution.

        :returns: random number
        :rtype: float
        """
        return random.uniform(-amount, amount)  # noqa: S311

    def _rand_laplace():
        """Generate a random number from the Laplace distribution.

        :returns: random number
        :rtype: float
        """
        # pylint: disable=no-member
        return np.random.laplace(0, amount)
        # pylint: enable=no-member

    def _rand_normal():
        """Generate a random number from the normal distribution.

        :returns: random number
        :rtype: float
        """
        return random.normalvariate(0, amount)

    def _rand_user():
        """Generate a random number from a user-defined function.

        :returns: random number
        :rtype: float
        """
        return rfunc(amount)

    if callable(rfunc):
        _rand = _rand_user
    elif rfunc == 'uniform':
        _rand = _rand_uniform
    elif rfunc == 'laplace':
        _rand = _rand_laplace
    else:
        _rand = _rand_normal

    newnums = [i + _rand() for i in nums]

    # Check that we haven't introduced values that exceed specified bounds
    # and aren't too far outside of normal
    # (This is an addition to the standard R algorithm)
    for i in range(len(newnums)):
        while newnums[i] < min_val or newnums[i] > max_val:
            newnums[i] = (newnums[i] + _rand())  # pragma: no cover

    # In the unlikely event that two equal values are in the list, try again
    if len(newnums) != len(set(newnums)):
        newnums = jitter(nums, factor, amount,
                         min_val, max_val)  # pragma: no cover

    return newnums
