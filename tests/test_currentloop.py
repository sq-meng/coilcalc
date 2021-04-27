import magcoilcalc


def test_magnet_creation():
    mag = magcoilcalc.CurrentLoop([-50, 10], 10, 101, 2.0, 3, 1)
    assert len(mag.start) == 2
    assert mag.nturns == 101
    assert all(mag.radius == [10, 10])
    assert all(mag.start == [-50, 10])
    assert mag.get_loop_list().shape == (101, 3)
    assert mag.get_loop_list()[-1][1] == 12


def test_magnet_get_field():
    mag = magcoilcalc.CurrentLoop([-50, 10], 10, 101, 2.0, 3, 1)
    mag.b_field(0, 0)
    mag.b_field(10, 0)