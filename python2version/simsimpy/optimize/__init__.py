"""Optimization module of SimSimPy package.

Contains some optimization functions, or functions for optimizations.
Depends on numpy and scipy.optimize
scipy_nlopt_cobyla will not work without nlopt
"""

__all__ = ["brute", "walk_search", "nlopt_wrap"]

from brute import brute
from walk_search import generate_all_directions
from walk_search import generate_nondiagonal_directions
from walk_search import test_nearby_points
from walk_search import walk, scipy_walk
from walk_search import graduate_walk, scipy_graduate_walk
from nlopt_wrap import scipy_nlopt_cobyla
