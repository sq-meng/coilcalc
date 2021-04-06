import coilcalc
import coilcalc.calculations


def test_fom():
    mag = coilcalc.CurrentLoop([-150, 150], 100, 420, 1)
    mag2 = coilcalc.CurrentLoop([-150, -150 + 63 * 40 / 63, 101], [101, 101], 63, 1, layers=2)
    mag3 = coilcalc.CurrentLoop([150 - 63 * 40 / 63, 150], [101, 101], 63, 1, layers=2)
    mesh = coilcalc.Mesh([-100, 100], [-50, 50], 61, 51)
    a = coilcalc.Task([mag, mag2, mag3], mesh)
    a.run()
    coilcalc.calculations.fom_cylindrical_cell(a, 50, 30)
