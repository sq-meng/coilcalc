"""
This example demonstrates how template functions should be used. The templates module contains a few frequently used
geometries.
"""

import coilcalc
import coilcalc.plotting
import coilcalc.calculations
import coilcalc.templates
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    coils = coilcalc.templates.helmholtz_coil(r=300)
    mesh = coilcalc.Mesh([-200, 200], [-200, 200], 100, 100)
    task = coilcalc.Task(coils, mesh)
    # Runs the calculations.
    task.run()
    # Plots intensity and lateral field gradient.
    coilcalc.plotting.draw_intensity(task, cell_length=80, cell_diameter=60)
    coilcalc.plotting.draw_normalized_gradient(task, cell_length=80, cell_diameter=60)
    # Calculates and prints Figure-of-Merit
    print("FoM: %f" % coilcalc.calculations.fom_cylindrical_cell(task, length=80, diameter=60))
    # stops the figures from disappearing
    plt.show()