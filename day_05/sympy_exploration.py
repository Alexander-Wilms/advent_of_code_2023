from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy.plotting import plot
from sympy.utilities.lambdify import lambdify

# The mappings can be represented as discontinuous functions mapping input values to output values.
# This way, one doesn't have to perform the mapping for each of the input values, but can do
# this symbolically through function composition (https://en.wikipedia.org/wiki/Function_composition).
# The resulting function can be evaluated using a vector of input values and the minimum output value determined.

x = sp.Symbol("x")

f1 = sp.Piecewise((x - 40, ((x >= 50) & (x <= 60))), (1, ((x < 50) | (x > 60))))
sp.pprint(f1, use_unicode=True)
plot(f1, (x, 0, 100))

f2 = sp.Piecewise((x - 65, ((x >= 70) & (x <= 80))), (50, ((x < 70) | (x > 80))))
sp.pprint(f2, use_unicode=True)
plot(f2, (x, 0, 100))

sp.pprint(f1 * f2, use_unicode=True)
# sqrt corrects for the multiplication of values
# not necessary, since sqrt(x) is strictly monotonic, but plot is easier to understand
f3 = sp.sqrt(f1 * f2)
plot(f3, (x, 0, 100))

print("evaluate symbolic expression")
# https://stackoverflow.com/a/10683911/2278742
func = lambdify(x, f3, "numpy")
x = np.arange(1, 100)
y = func(x)
print(f"{x=}")
print(f"{y=}")

plt.plot(x, y)
plt.show()

print("x where f(x) == min(f(x)):")
# print(np.min(y[40:]))
# print(np.argmin(numpy.array(y[40:])))
pprint(np.where(y == y.min()))
