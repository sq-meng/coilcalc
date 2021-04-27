"""
This example demonstrates how template functions should be used. The templates module contains a few frequently used
geometries.
"""

import magcoilcalc
import magcoilcalc.plotting
import magcoilcalc.calculations
import magcoilcalc.templates
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # call the template function - check the module yourself for usages.
    coils = magcoilcalc.templates.helmholtz_coil(r=300)
    # Create a mesh from x = -200 to 200, y = -200 t0 200, 100 steps each
    mesh = magcoilcalc.Mesh([-200, 200], [-200, 200], 100, 100)
    # Puts the two into a Task object.
    task = magcoilcalc.Task(coils, mesh)
    # Runs the calculations.
    task.run()
    # Plots intensity and lateral field gradient.
    magcoilcalc.plotting.draw_intensity(task, cell_length=80, cell_diameter=60)
    magcoilcalc.plotting.draw_normalized_gradient(task, cell_length=80, cell_diameter=60)
    # Calculates and prints Figure-of-Merit
    print("FoM: %f" % magcoilcalc.calculations.fom_cylindrical_cell(task, length=80, diameter=60))
    # stops the figures from disappearing
    plt.show()
