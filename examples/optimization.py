"""
Example on how to use scipy.optimize.minimize to find the optimal design
"""

from scipy.optimize import minimize
import magcoilcalc
import magcoilcalc.plotting
import magcoilcalc.calculations
import matplotlib.pyplot as plt
import numpy as np


# constructs a function that takes one length parameter, and return a Task object.
def construction_func(length):
    # constructs a Helmholtz-like coil, with one variable open to optimization.
    r = 400
    # length (distance between coils) open to optimization.
    l = length
    bobbin_width = 10
    nturns = 100
    current = 1.0
    winding_layers = 10
    wire_diameter = 1.0
    # derived bobbin construction parameters
    bobbin_xspan = np.array([l / 2 - bobbin_width / 2, l / 2 + bobbin_width / 2])
    bobbin_radius = r - winding_layers * wire_diameter / 2
    # Build "left" coil

    c1 = magcoilcalc.CurrentLoop(-bobbin_xspan, bobbin_radius, nturns, current,
                                 layers=winding_layers, layer_thickness=wire_diameter)
    # Build "right" coil
    c2 = magcoilcalc.CurrentLoop(bobbin_xspan, bobbin_radius, nturns, current,
                                 layers=winding_layers, layer_thickness=wire_diameter)
    # Create a mesh from x = -120 to 120, y = -100 t0 100, 100 steps each
    mesh = magcoilcalc.Mesh([-120, 120], [-50, 50], 50, 50)
    # Puts the two into a Task object.
    task = magcoilcalc.Task([c1, c2], mesh)
    return task


# the optimization function unwraps the parameter array and feed the only member to the construction function,
# run the calculation, and return the optimization target value.
def opt_func(pars):
    task = construction_func(pars[0])
    # Runs the calculations.
    task.run()
    # Calculates FoM and return the value.
    return magcoilcalc.calculations.fom_cylindrical_cell(task, 180, 60)


if __name__ == '__main__':
    # initialize the minimizer routine
    initial_l = 350
    res = minimize(opt_func, x0=np.array(initial_l), tol=0.02)
    optimal_l = res.x[0]
    print(res)
    t1 = construction_func(initial_l)
    t2 = construction_func(optimal_l)
    t1.run(), t2.run()
    magcoilcalc.plotting.draw_normalized_gradient(t1, cell_length=180, cell_diameter=60)
    magcoilcalc.plotting.draw_normalized_gradient(t2, cell_length=180, cell_diameter=60)
    plt.show()
