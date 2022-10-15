import magcoilcalc
import numpy as np
from numba import jit
from magcoilcalc._current_sheet import field_radial


@jit
def jit_fr(i_tot, a, length, z_list, r_list):
    out = []
    for z, r in zip(z_list, r_list):
        out.append(field_radial(5, 100, 10, z, r))
