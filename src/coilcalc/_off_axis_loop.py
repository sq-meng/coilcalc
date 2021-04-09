from scipy.special import ellipe, ellipk
from numpy import pi, sqrt, sin, linspace, sum, power
import numpy as np

u0 = 4e-7 * pi


def B0(i, a, u=u0):
    return i * u / 2.0 / a


def alpha(r, a):
    return r / a


def beta(x, a):
    return x / a


def gamma(x, r):
    return x / r


def Q(r, x, a):
    return (1 + alpha(r, a)) ** 2 + beta(x, a) ** 2


def k(r, x, a):
    return sqrt(4 * alpha(r, a) / Q(r, x, a))


def K(x):
    return ellipk(x ** 2)


def E(x):
    return ellipe(x ** 2)


def Baxial(i, a, x, u=u0):
    return (u * i * a ** 2) / 2 / (a ** 2 + x ** 2) ** 1.5


def field_axial(i, a, x, r):
    # sign of r not important here
    r = np.abs(r)
    return B0(i, a) * (E(k(r, x, a)) * (1 - alpha(r, a) ** 2 - beta(x, a) ** 2) / (Q(r, x, a) - 4 * alpha(r, a)) +
                           K(k(r, x, a))) / pi / sqrt(Q(r, x, a))


def field_radial(i, a, x, r):
    """

    :param i: current in amps
    :param a: loop radius in meters.
    :param x: distance from loop plane in meters.
    :param r: distance from loop axis in meters.
    :return: field at (x, r) in Tesla.
    """
    sr = np.sign(r)
    r = np.abs(r)
    try:
        # if r is not an array and equals to 0.
        if r == 0:
            return 0
        # if r is an array this will trigger.
    except ValueError:
        pass
    res = B0(i, a) * gamma(x, r) * \
           (E(k(r, x, a)) * (1 + alpha(r, a) ** 2 + beta(x, a) ** 2) / (Q(r, x, a) - 4 * alpha(r, a)) -
                                     K(k(r, x, a))) / pi / sqrt(Q(r, x, a))
    try:
        # This only works if r is an array.
        res[r == 0] = 0
    except TypeError:
        # r is not an array, but is also not zero.
        pass
    return res * sr
