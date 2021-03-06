import magcoilcalc
import numpy as np


def test_current_sheet_spawn():
    cs = magcoilcalc.CurrentSheet([-50, 10], 10, 50, 1.2)
    assert len(cs.start) == 2
    assert cs.nturns == 50
    assert all(cs.radius == [10, 10])
    assert all(cs.start == [-50, 10])


def test_current_sheet_get_field():
    cs = magcoilcalc.CurrentSheet([-50, 10], 10, 50, 1.2)
    cs.b_field(0, 0)
    cs.b_field(20, 20)
    cs.b_field(-20, 20)


def test_agreement_sheet_and_loop():
    cs = magcoilcalc.CurrentSheet([-180, 180], 123, 300, 1)
    cl = magcoilcalc.CurrentLoop([-180, 180], 123, 300, 1)
    xl = np.linspace(-300, 300, 10)
    yl = np.linspace(-100, 100, 10)
    xg, yg = np.meshgrid(xl, yl)
    xgl = xg.flatten()
    ygl = yg.flatten()

    for x, y in zip(xgl, ygl):
        assert np.all(np.isclose(cs.b_field(x, y), cl.b_field(x, y), rtol=2e-2))


def test_add_currentsheet():
    cs = magcoilcalc.CurrentSheet([-180, 180], 123, 300, 1)
    mesh = magcoilcalc.Mesh([-20, 20], [-10, 10], 21, 21)
    t = magcoilcalc.Task([cs], mesh)
    t.run()
