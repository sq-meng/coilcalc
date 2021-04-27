import magcoilcalc
import magcoilcalc.calculations
import magcoilcalc.templates


def test_1d_scan():
    def fun(x):
        magnets = magcoilcalc.templates.helmholtz_coil(r=x)
        mesh = magcoilcalc.Mesh([-100, 100], [-50, 50], 51, 31)
        task = magcoilcalc.Task(magnets, mesh)
        task.run()
        return magcoilcalc.calculations.fom_cylindrical_cell(task, 100, 60)
    res = magcoilcalc.calculations.parameter_scan(fun, [200, 300, 5])


def test_2d_scan():
    def fun(x, y):
        magnets = magcoilcalc.templates.helmholtz_coil(r=x, coil_width=y)
        mesh = magcoilcalc.Mesh([-100, 100], [-50, 50], 51, 31)
        task = magcoilcalc.Task(magnets, mesh)
        task.run()
        return magcoilcalc.calculations.fom_cylindrical_cell(task, 100, 60)
    res = magcoilcalc.calculations.parameter_scan(fun, [200, 300, 2], [10, 20, 3])


def test_3d_scan():
    def fun(x, y, z):
        magnets = magcoilcalc.templates.helmholtz_coil(r=x, coil_width=y, current=z)
        mesh = magcoilcalc.Mesh([-100, 100], [-50, 50], 51, 31)
        task = magcoilcalc.Task(magnets, mesh)
        task.run()
        return magcoilcalc.calculations.fom_cylindrical_cell(task, 100, 60)
    res = magcoilcalc.calculations.parameter_scan(fun, [200, 300, 2], [10, 20, 2], [0.5, 1.5, 3])
