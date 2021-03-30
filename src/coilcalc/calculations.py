import numpy as np


def find_gradient(task, lat_field_axis='y', gradient_axes="xyt"):
    """
    Finds the lateral field gradient in given axes.
    :param task: completed task object.
    :param lat_field_axis: Which field component should be calculated. Doesn't make sense except y direction, really.
    :param gradient_axes: Gradient along which directions are considered. xy: gradient in the axial plane. xyt: xy plus
    the tangential gradient.
    :return: An array describing the field gradient figure.
    """
    if lat_field_axis == 'y':
        lat_field = task.y_field
    elif lat_field_axis == 'x':
        lat_field = task.x_field
    else:
        raise ValueError("Gradient calculation: lat_field_axis accepts x, y, xy or xyt.")

    gradient_y = np.gradient(lat_field, task.mesh.y_step / 10, axis=0)
    gradient_x = np.gradient(lat_field, task.mesh.x_step / 10, axis=1)
    if gradient_axes == 'xyt':
        g_axial_plane = np.sqrt(gradient_y ** 2 + gradient_x ** 2)
        y_mesh_nonzero = task.y_mesh.copy()
        y_mesh_nonzero[y_mesh_nonzero==0] = 1
        g_tangent = task.y_field / y_mesh_nonzero * 10
        g = np.sqrt(g_axial_plane ** 2 + g_tangent ** 2)

    elif gradient_axes == 'xy':
        g = np.sqrt(gradient_y ** 2 + gradient_x ** 2)
    elif gradient_axes == 'y':
        g = np.abs(gradient_y)
    elif gradient_axes == 'x':
        g = np.abs(gradient_x)
    else:
        raise ValueError("Gradient calculation: gradient axes accepts x or y or xy.")
    return g


def fom_cylindrical_cell(task, length, diameter, xsteps=51, ysteps=51):
    if not task.done:
        raise ValueError("FOM calculation: Field not solved.")
    if task.mesh.x_range[0] > -length / 2 or \
            task.mesh.x_range[1] < length / 2 or \
            task.mesh.y_range[0] > -diameter / 2 or \
            task.mesh.y_range[1] < diameter / 2:
        raise ValueError("FOM calculation: mesh doesn't cover cell area.")
    ls_x = np.linspace(-length/2, length/2, xsteps)
    ls_y = np.linspace(-diameter/2, diameter/2, ysteps)
    xg, yg = np.meshgrid(ls_x, ls_y)
    x_list = xg.flatten()
    y_list = yg.flatten()
    center_field = task.center_field
    weights = abs(y_list) / sum(abs(y_list))
    gradient_interpolator = task.make_gradient_interpolator()
    gradients = gradient_interpolator(np.vstack((x_list, y_list)).T) / center_field[0]
    return 1 / (5e-4 / np.sum(gradients * weights))


def _check_param(param):
    pass


def parameter_scan(func, parx=None, pary=None, parz=None, fom_func=fom_cylindrical_cell, processes=1):
    if parx is None and pary is None and parz is None:
        raise ValueError("parameter scan: at least 1 parameter required")

    if parx is not None and pary is None and parz is None:
        xg = np.linspace(*parx)
        x_list = xg.flatten()
        fom = [func(x) for x in x_list]
        return list(fom), xg

    if parx is not None and pary is not None and parz is None:
        x_ls = np.linspace(*parx)
        y_ls = np.linspace(*pary)
        xg, yg = np.meshgrid(x_ls, y_ls)
        x_list = xg.flatten()
        y_list = yg.flatten()
        if processes == 1:
            fom = np.array([func(x, y) for x, y in zip(x_list, y_list)]).reshape(xg.shape)
            return fom, xg, yg
        else:
            raise NotImplementedError

    if parx is not None and pary is not None and parz is not None:
        x_ls = np.linspace(*parx)
        y_ls = np.linspace(*pary)
        z_ls = np.linspace(*parz)
        yg, zg, xg = np.meshgrid(y_ls, z_ls, x_ls)
        x_list = xg.flatten()
        y_list = yg.flatten()
        z_list = zg.flatten()
        if processes == 1:
            fom = np.array([func(x, y, z) for x, y, z in zip(x_list, y_list, z_list)]).reshape(xg.shape)
            return fom, xg, yg
        else:
            raise NotImplementedError

    else:
        raise ValueError("Parameter scan: invalid combination of parameters received")
