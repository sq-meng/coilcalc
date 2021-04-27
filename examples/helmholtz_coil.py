"""
This example demonstrates how a coil is defined and simulated.
"""

import magcoilcalc
import magcoilcalc.plotting
import magcoilcalc.calculations
import matplotlib.pyplot as plt
import numpy as np


# Only runs this part if the script is actually "run" instead of imported.
if __name__ == "__main__":
    # Physical parameters
    r = 400
    l = r
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
    mesh = magcoilcalc.Mesh([-120, 120], [-100, 100], 100, 100)
    # Puts the two into a Task object.
    task = magcoilcalc.Task([c1, c2], mesh)
    # Runs the calculations.
    task.run()
    # Plots intensity and lateral field gradient.
    magcoilcalc.plotting.draw_intensity(task, cell_length=80, cell_diameter=60)
    magcoilcalc.plotting.draw_normalized_gradient(task, cell_length=80, cell_diameter=60)
    # Calculates and prints Figure-of-Merit
    print("FoM: %f" % magcoilcalc.calculations.fom_cylindrical_cell(task, length=80, diameter=60))
    # stops the figures from disappearing
    plt.show()
