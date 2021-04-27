import magcoilcalc
import magcoilcalc.calculations


def test_fom():
    mag = magcoilcalc.CurrentLoop([-150, 150], 100, 420, 1)
    mag2 = magcoilcalc.CurrentLoop([-150, -150 + 63 * 40 / 63, 101], [101, 101], 63, 1, layers=2)
    mag3 = magcoilcalc.CurrentLoop([150 - 63 * 40 / 63, 150], [101, 101], 63, 1, layers=2)
    mesh = magcoilcalc.Mesh([-100, 100], [-50, 50], 61, 51)
    a = magcoilcalc.Task([mag, mag2, mag3], mesh)
    a.run()
    magcoilcalc.calculations.fom_cylindrical_cell(a, 50, 30)
