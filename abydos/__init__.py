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

"""abydos.

Abydos NLP/IR library by Christopher C. Little
"""
__all__ = ['clustering', 'compression', 'corpus', 'distance', 'fingerprint',
           'ngram', 'phones', 'phonetic', 'qgram', 'stats', 'stemmer']

from .clustering import *
from .compression import *
from .corpus import *
from .distance import *
from .fingerprint import *
from .ngram import *
from .phones import *
from .phonetic import *
from .qgram import *
from .stats import *
from .stemmer import *

if __name__ == '__main__':
    pass