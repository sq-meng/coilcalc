from coilcalc._mpl_wrap import *

import matplotlib.pyplot as plt
import numpy as np
from coilcalc.core import Task, Magnet, Mesh
from matplotlib.pyplot import Rectangle, Circle
from coilcalc.calculations import find_gradient
from matplotlib.colors import LogNorm, Normalize


def draw_cell_boundary(ax, width, height, x_offset=0, y_offset=0, color=(0.8, 0.8, 0.8)):
    r = Rectangle((-width/2 + x_offset, -height/2 + y_offset), width, height,
                  fill=False, linewidth=1, edgecolor=color, linestyle='--')
    ax.plot(x_offset, y_offset, 'b+', color=color)
    ax.add_artist(r)
    return r


def draw_mesh_boundary(mesh: Mesh, ax):
    width = mesh.x_range[1] - mesh.x_range[0]
    height = mesh.y_range[1] - mesh.y_range[0]
    r = Rectangle((-width/2, -height/2), width, height,
                  fill=False, linewidth=0.5, edgecolor='black', linestyle='--', zorder=20)
    ax.add_artist(r)


def draw_magnet(ax, magnet: Magnet):
    c1 = np.asarray(magnet.get_loop_list())
    c2 = c1 * [1, -1, 1]
    try:
        dia = np.sqrt(np.power(c1[0][0] - c1[1][0], 2) + np.power(c1[0][1] - c1[1][1], 2))
        dia = min(dia, 1.0)
    except IndexError:
        dia = 1.0
    neg = np.asarray([1, -1])
    poly = plt.Polygon((magnet.start, magnet.end,  magnet.end * neg, magnet.start * neg), color=[0.4, 0.4, 0.4, 0.25],
                       zorder=0)
    ax.add_artist(poly)
    for loop in c1:
        circle = Circle((loop[0], loop[1]), dia/2, fill=None)
        ax.add_artist(circle)
    for loop in c2:
        circle = Circle((loop[0], loop[1]), dia/2, fill=None)
        ax.add_artist(circle)


def draw_normalized_gradient(cal: Task, cmap='inferno', norm=None, field_axis='y', gradient_axes='xy', vmin=0.0001,
                             vmax=0.01, ax=None, colorbar=True, cell_length=100, cell_diameter=60):
    if norm is None:
        norm = LogNorm(vmin=vmin, vmax=vmax)

    if ax is None:
        f, ax = plt.subplots()
    else:
        f = ax.figure
    for magnet in cal.magnets:
        draw_magnet(ax, magnet)
    gradient = find_gradient(cal, lat_field_axis=field_axis, gradient_axes=gradient_axes) / cal.center_field[0]
    contour_plot = ax.contour(cal.x_mesh, cal.y_mesh, np.abs(gradient), [2e-4, 5e-4, 1e-3, 2e-3, 0.005],
                              colors='w', zorder=10)
    # to avoid values smaller than vmin not being able to render
    gradient[gradient < norm.vmin] = norm.vmin
    color_plot = ax.pcolor(cal.x_pixel_bounds, cal.y_pixel_bounds, np.abs(gradient), norm=norm, cmap=cmap)
    ax.clabel(contour_plot, fontsize=10, inline=1, fmt='%.4f')
    ax.axis('equal')
    draw_cell_boundary(ax, cell_length, cell_diameter)
    draw_mesh_boundary(cal.mesh, ax)
    if colorbar:
        color_bar = f.colorbar(color_plot)
        color_bar.ax.set_ylabel('%s field gradient 1/cm' % gradient_axes)
    # labels

    ax.set_xlabel('Position / mm, axial ')
    ax.set_ylabel('Position / mm, radial')
    ax.autoscale()

    return color_plot, f, ax


def draw_intensity(cal: Task, cmap='inferno', norm=None, field_axis='x', vmin=0.98,
                             vmax=1.02, ax=None, colorbar=True, cell_length=100, cell_diameter=60):
    if norm is None:
        norm = Normalize()
    if ax is None:
        f, ax = plt.subplots()
    else:
        f = ax.figure
    for magnet in cal.magnets:
        draw_magnet(ax, magnet)
    if field_axis == 'x':
        field = cal.x_field
    elif field_axis == 'y':
        field = cal.y_field
    else:
        raise ValueError("Intensity plot: only x or y accepted for field axis, got %s " % field_axis)
    norm.vmin = cal.center_field[0] * vmin
    norm.vmax = cal.center_field[0] * vmax

    color_plot = ax.pcolor(cal.x_mesh, cal.y_mesh, field, norm=norm, cmap=cmap)
    ax.axis('equal')
    draw_cell_boundary(ax, cell_length, cell_diameter)
    draw_mesh_boundary(cal.mesh, ax)
    if colorbar:
        color_bar = f.colorbar(color_plot)
        color_bar.ax.set_ylabel('%s field/ Tesla' % field_axis)
    # labels

    ax.set_xlabel('Position / mm, axial')
    ax.set_ylabel('Position / mm, radial')
    ax.autoscale()
    return color_plot, f, ax
