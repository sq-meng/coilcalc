"""
Source:
https://tiggerntatie.github.io/emagnet-py/offaxis/off_axis_loop.html
Used to test against implementation in this package
Included under the MIT license
"""
from scipy.special import ellipk, ellipe
from numpy import pi, sqrt, NaN

uo = 4E-7 * pi  # Permeability constant - units of H/m
Bo = lambda i, a, u=uo: i * u / 2. / a  # Central field = f(current, loop radius, perm. constant)
al = lambda r, a: r / a  # Alpha = f(radius of measurement point, radius of loop)
be = lambda x, a: x / a  # Beta = f(axial distance to meas. point, radius of loop)
ga = lambda x, r: x / r  # Gamma = f(axial distance, radius to meas. point)
Q = lambda r, x, a: (1 + al(r, a)) ** 2 + be(x, a) ** 2  #
# Q = f(radius, distance to meas. point, loop radius)
k = lambda r, x, a: sqrt(4 * al(r, a) / Q(r, x, a))  # k = f(radius, distance to meas. point, loop radius)
K = lambda k: ellipk(k ** 2.0)  # Elliptic integral, first kind, as a function of k
E = lambda k: ellipe(k ** 2.0)  # Elliptic integral, second kind, as a function of k


# On-Axis field = f(current and radius of loop, x of measurement point)
def Baxial(i, a, x, u=uo):
    if a == 0:
        if x == 0:
            return NaN
        else:
            return 0.0
    else:
        return (u * i * a ** 2) / 2.0 / (a ** 2 + x ** 2) ** 1.5


# Axial field component = f(current and radius of loop, r and x of meas. point)
def field_axial(i, a, x, r):
    if r == 0:
        if x == 0:
            return Bo(i, a)  # central field
        else:
            return Baxial(i, a, x)  # axial field
    else:  # axial component, any location
        return Bo(i, a) * \
               (E(k(r, x, a)) * ((1.0 - al(r, a) ** 2 - be(x, a) ** 2) / (Q(r, x, a) - 4 * al(r, a))) + K(k(r, x, a))) \
               / pi / sqrt(Q(r, x, a))


# Radial field component = f(current and radius of loop, r and x of meas. point)
def field_radial(i, a, x, r):
    if r == 0:
        return 0.0  # no radial component on axis!
    else:  # radial component, any location other than axis.
        return Bo(i, a) * ga(x, r) * \
               (E(k(r, x, a)) * ((1.0 + al(r, a) ** 2 + be(x, a) ** 2) / (Q(r, x, a) - 4 * al(r, a))) - K(k(r, x, a))) \
               / pi / sqrt(Q(r, x, a))