import coilcalc
import coilcalc.calculations
import coilcalc.templates


def test_1d_scan():
    def fun(x):
        magnets = coilcalc.templates.helmholtz_coil(r=x)
        mesh = coilcalc.Mesh([-100, 100], [-50, 50], 51, 31)
        task = coilcalc.Task(magnets, mesh)
        task.run()
        return coilcalc.calculations.fom_cylindrical_cell(task, 100, 60)
    res = coilcalc.calculations.parameter_scan(fun, [200, 300, 5])


def test_2d_scan():
    def fun(x, y):
        magnets = coilcalc.templates.helmholtz_coil(r=x, coil_width=y)
        mesh = coilcalc.Mesh([-100, 100], [-50, 50], 51, 31)
        task = coilcalc.Task(magnets, mesh)
        task.run()
        return coilcalc.calculations.fom_cylindrical_cell(task, 100, 60)
    res = coilcalc.calculations.parameter_scan(fun, [200, 300, 2], [10, 20, 3])


def test_3d_scan():
    def fun(x, y, z):
        magnets = coilcalc.templates.helmholtz_coil(r=x, coil_width=y, current=z)
        mesh = coilcalc.Mesh([-100, 100], [-50, 50], 51, 31)
        task = coilcalc.Task(magnets, mesh)
        task.run()
        return coilcalc.calculations.fom_cylindrical_cell(task, 100, 60)
    res = coilcalc.calculations.parameter_scan(fun, [200, 300, 2], [10, 20, 2], [0.5, 1.5, 3])
