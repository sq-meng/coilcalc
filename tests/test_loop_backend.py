import magcoilcalc._off_axis_loop as m1
import magcoilcalc._loop_calc_dennison as m2
import numpy as np


# Tests vectorized implementation
# TODO: find the warning.
def test_coil_integrity():
    numbers = np.load('rand.npy')
    numbers[0:50, 0] = 0
    numbers[51:200, 2] = 0
    numbers[100:200, 3] = 0
    r1x = m1.field_axial(numbers[:, 0], numbers[:, 1], numbers[:, 2], numbers[:, 3])
    r1r = m1.field_radial(numbers[:, 0], numbers[:, 1], numbers[:, 2], numbers[:, 3])
    r2x = [m2.field_axial(*line) for line in numbers]
    r2r = [m2.field_radial(*line) for line in numbers]

    assert np.allclose(r1x, r2x)
    assert np.allclose(r1r, r2r)
    assert np.isclose(m1.field_axial(2.2, 5, 3, 1), 1.7293349e-07)
    assert np.isclose(m1.field_axial(2.2, 5, 3, -1), 1.7293349e-07)
