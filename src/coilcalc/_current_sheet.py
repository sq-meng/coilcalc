import numpy as np
from scipy.integrate import quad
from numpy import pi


u0 = 4e-7 * pi


def cel_func(phi, kc, p, c, s):
    return (c * np.cos(phi) ** 2 + s * np.sin(phi) ** 2) / \
           ((np.cos(phi) ** 2 + p * np.sin(phi) ** 2) * np.sqrt(np.cos(phi) ** 2 + kc ** 2 * np.sin(phi) ** 2))


def cel(kc, p, c, s):
    return quad(cel_func, 0, pi / 2, (kc, p, c, s))[0]


def field_radial(Itot, a, l, z, r):
    (a, l, z, r) = (a / 1000, l / 1000, z / 1000, r / 1000)
    b = l / 2
    I = Itot / l
    b0 = u0 / pi * I
    zplus = z + b
    zminus = z - b
    alpha_plus = a / np.sqrt(zplus ** 2 + (r + a) ** 2)
    alpha_minus = a / np.sqrt(zminus ** 2 + (r + a) ** 2)
    kplus = np.sqrt((zplus ** 2 + (a - r) ** 2)/(zplus ** 2 + (a + r) ** 2))
    kminus = np.sqrt((zminus ** 2 + (a - r) ** 2)/(zminus ** 2 + (a + r) ** 2))
    return b0 * (alpha_plus * cel(kplus, 1, 1, -1) - alpha_minus * cel(kminus, 1, 1, -1))


def field_axial(Itot, a, l, z, r):
    (a, l, z, r) = (a / 1000, l / 1000, z / 1000, r / 1000)
    b = l / 2
    I = Itot / l
    b0 = u0 / pi * I
    zplus = z + b
    zminus = z - b
    alpha_plus = a / np.sqrt(zplus ** 2 + (r + a) ** 2)
    alpha_minus = a / np.sqrt(zminus ** 2 + (r + a) ** 2)
    beta_plus = zplus / np.sqrt(zplus ** 2 + (r + a) ** 2)
    beta_minus = zminus / np.sqrt(zminus ** 2 + (r + a) ** 2)
    gamma = (a - r) / (a + r)
    kplus = np.sqrt((zplus ** 2 + (a - r) ** 2) / (zplus ** 2 + (a + r) ** 2))
    kminus = np.sqrt((zminus ** 2 + (a - r) ** 2) / (zminus ** 2 + (a + r) ** 2))
    return b0 * a / (a + r) * (beta_plus * cel(kplus, gamma ** 2, 1, gamma) - beta_minus * cel(kminus, gamma ** 2, 1, gamma))