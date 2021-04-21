"""
This example defines a function that builds a Helmholtz coil from a few parameters. The magnetic field of the coil is
then simulated.
"""

import coilcalc
import coilcalc.plotting
import coilcalc.calculations

import matplotlib.pyplot as plt


# Only runs this part if the script is actually "run" instead of imported.
if __name__ == "__main__":
    r = 400
    bobbin_width = 10
    nturns = 100
    current = 1.0
    winding_layers = 10
    wire_diameter = 1.0
    # Build "left" coil

    c1 = coilcalc.CurrentLoop([-r / 2 - bobbin_width / 2, -r / 2 + bobbin_width / 2], r, nturns, current,
                              layers=winding_layers, layer_thickness=wire_diameter)
    # Build "right" coil
    c2 = coilcalc.CurrentLoop([r / 2 - bobbin_width / 2, r / 2 + bobbin_width / 2], r, nturns, current,
                              layers=winding_layers, layer_thickness=wire_diameter)
    # Create a mesh from x = -120 to 120, y = -100 t0 100, 100 steps each
    mesh = coilcalc.Mesh([-120, 120], [-100, 100], 100, 100)
    # Puts the two into a Task object.
    task = coilcalc.Task([c1, c2], mesh)
    # Runs the calculations.
    task.run()
    # Plots intensity and lateral field gradient.
    coilcalc.plotting.draw_intensity(task, cell_length=80, cell_diameter=60)
    coilcalc.plotting.draw_normalized_gradient(task, cell_length=80, cell_diameter=60)
    # Calculates and prints Figure-of-Merit
    print("FoM: %f" % coilcalc.calculations.fom_cylindrical_cell(task, length=80, diameter=60))
    # stops the figures from disappearing
    plt.show()
