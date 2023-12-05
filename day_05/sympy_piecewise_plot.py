# https://github.com/sympy/sympy/issues/17738

import sympy as sp
from sympy.plotting import plot

x = sp.Symbol("x")
f = sp.Piecewise((-(x**2) / 2 + 1, x <= 0), (x**2 / 2, True))

plt = plot(f, (x, -2, 2))
