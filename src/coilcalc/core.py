from coilcalc._mpl_wrap import *
import numpy as np
import coilcalc._off_axis_loop as loop_calculator
from scipy.interpolate import RegularGridInterpolator, LinearNDInterpolator
from coilcalc.calculations import find_gradient
from itertools import product
from coilcalc._signals import logger
from matplotlib.pyplot import Rectangle, Circle, Polygon
import coilcalc._current_sheet as sheet_calculator
try:
    import multiprocessing
except ImportError:
    multiprocessing = None


class CurrentLoop(object):
    def __init__(self, x_span: (list, float, int), radius: (list, float, int), nturns: int, current: float,
                 layers: int = 1, layer_thickness: float = 1.0, current_multiplier: float = 1.0):
        """
        :param x_span: [x, y] coordinates for one end of the coil, in mm.
        :param radius: [x, y] for the other end, in mm.
        :param nturns: number of turns.
        :param current: current in amps.
        :param layers: Number of layers of coil that is wound on top of each other.
        :param layer_thickness: Thickness of each winding layer in mm.
        """
        self._x_span = None
        self._radius = None
        self._nturns = None
        self._reverse_polarity = None
        self._current = None
        self._layers = None
        self._layer_thickness = None
        self._current_multiplier = None
        self.x_span = x_span
        self.radius = radius
        self.nturns = nturns
        self.current = current
        self.layers = layers
        self.layer_thickness = layer_thickness
        self.current_multiplier = current_multiplier

    @property
    def x_span(self):
        return self._x_span

    @x_span.setter
    def x_span(self, value):
        try:
            _ = value[1]
            self._x_span = value
        except (TypeError, IndexError, ValueError):
            self._x_span = [value, value]

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        try:
            _ = value[1]
            self._radius = value
        except (TypeError, IndexError, ValueError):
            self._radius = [value, value]

    @property
    def start(self):
        """
        (x, y) coordinates of where the coil starts.
        :return: (x, y) in mm.
        """
        return [self._x_span[0], self._radius[0]]

    @property
    def end(self):
        """
        (x, y) coordinates of where the coil ends.
        :return: (x, y) in mm.
        """
        return [self._x_span[1], self._radius[1]]

    @property
    def nturns(self):
        return self._nturns

    @nturns.setter
    def nturns(self, value):
        if value >= 1:
            self._nturns = int(value)
        else:
            raise ValueError("Magnet: cannot define a magnet with less than 1 turn.")

    @property
    def current(self):
        """
        Current in the coil, amps.
        :return: float.
        """
        return self._current

    @current.setter
    def current(self, value):
        self._current = value

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, value):
        if int(value) != value:
            raise TypeError("Magnet: integer expected for layers count.")
        elif value < 1:
            raise ValueError("Magnet: at least 1 layer required.")
        else:
            self._layers = value

    @property
    def layer_thickness(self):
        return self._layer_thickness

    @layer_thickness.setter
    def layer_thickness(self, value: float):
        self._layer_thickness = value

    @property
    def current_multiplier(self):
        return self._current_multiplier

    @current_multiplier.setter
    def current_multiplier(self, value: float):
        self._current_multiplier = value

    def __copy__(self):
        return CurrentLoop(self.x_span, self.radius, self.nturns, self.current, self.layers, self.layer_thickness)

    def get_loop_list(self):
        """
        A list defining each loop in the coil.
        :return: [x, r, current], x and r in mm, current in amps.
        """
        turns_per_layer = self.nturns // self.layers
        extra_turn_layers = self.nturns % self.layers
        coil_layers = []
        for i in range(0, self.layers):
            if i < extra_turn_layers:
                turns = turns_per_layer + 1
            else:
                turns = turns_per_layer
            x = np.linspace(self.start[0], self.end[0], turns)
            y = np.linspace(self.start[1], self.end[1], turns) + i * self.layer_thickness
            this_layer = np.vstack([x, y, np.ones(turns) * self.current]).T
            coil_layers.append(this_layer)
        return np.vstack(coil_layers)

    def b_field(self, xp, yp):
        """
        Calculate the field at [xp, yp]
        :param xp: x coords, in mm.
        :param yp: y coords, in mm.
        :return: Field in Tesla.
        """
        bx = 0
        br = 0
        for loop in self.get_loop_list():
            a = loop[1] / 1000
            x = (xp - loop[0]) / 1000
            r = yp / 1000
            current = loop[2]
            bx += loop_calculator.field_axial(current, a, x, r)
            br += loop_calculator.field_radial(current, a, x, r)
        return bx, br

    def draw_source(self, ax):
        source = self
        c1 = np.asarray(source.get_loop_list())
        c2 = c1 * [1, -1, 1]
        try:
            dia = np.sqrt(np.power(c1[0][0] - c1[1][0], 2) + np.power(c1[0][1] - c1[1][1], 2))
            dia = min(dia, 1.0)
        except IndexError:
            dia = 1.0
        neg = np.asarray([1, -1])
        poly = Polygon((source.start, source.end, source.end * neg, source.start * neg),
                           color=[0.4, 0.4, 0.4, 0.25],
                           zorder=0)
        ax.add_artist(poly)
        for loop in c1:
            circle = Circle((loop[0], loop[1]), dia / 2, fill=None)
            ax.add_artist(circle)
        for loop in c2:
            circle = Circle((loop[0], loop[1]), dia / 2, fill=None)
            ax.add_artist(circle)


class CurrentSheet(object):
    def __init__(self, x_span: (list, float, int), radius, nturns: int, current: float, current_multiplier=1):
        self._x_span = None
        self._radius = None
        self._nturns = None
        self._reverse_polarity = None
        self._current = None
        self._current_multiplier = None
        self.x_span = x_span
        self.radius = radius
        self.nturns = nturns
        self.current = current
        self.current_multiplier = current_multiplier

    @property
    def x_span(self):
        return self._x_span

    @x_span.setter
    def x_span(self, value):
        try:
            _ = value[1]
            self._x_span = value
        except (TypeError, IndexError, ValueError):
            self._x_span = [value, value]

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        try:
            _ = value[1]
            self._radius = value
        except (TypeError, IndexError, ValueError):
            self._radius = [value, value]

    @property
    def start(self):
        """
        (x, y) coordinates of where the coil starts.
        :return: (x, y) in mm.
        """
        return [self._x_span[0], self._radius[0]]

    @property
    def end(self):
        """
        (x, y) coordinates of where the coil ends.
        :return: (x, y) in mm.
        """
        return [self._x_span[1], self._radius[1]]

    @property
    def nturns(self):
        return self._nturns

    @nturns.setter
    def nturns(self, value):
        if value >= 1:
            self._nturns = int(value)
        else:
            raise ValueError("Magnet: cannot define a magnet with less than 1 turn.")

    @property
    def current(self):
        """
        Current in the coil, amps.
        :return: float.
        """
        return self._current

    @current.setter
    def current(self, value):
        self._current = value

    @property
    def length(self):
        return np.abs(self.x_span[1] - self.x_span[0])

    def b_field(self, xp, yp):
        x_center = np.mean(self.x_span)
        x = xp - x_center
        rho = yp
        fr = sheet_calculator.field_radial(self.current * self.nturns, self.radius[0], self.length, x, rho)
        fx = sheet_calculator.field_axial(self.current * self.nturns, self.radius[0], self.length, x, rho)
        return (fx, fr)


class Mesh(object):
    def __init__(self, x_range=None, y_range=None, x_steps=None, y_steps=None):
        self._x_range = None
        self._y_range = None
        self._x_steps = None
        self._y_steps = None
        self.x_range = x_range
        self.y_range = y_range
        self.x_steps = x_steps
        self.y_steps = y_steps

    def get_matrix(self):
        """
        Returns the x and y coordinates in two (m, n) arrays.
        :return: x and y in (m, n) arrays.
        """
        x = np.linspace(self.x_range[0], self.x_range[1], self.x_steps)
        y = np.linspace(self.y_range[0], self.y_range[1], self.y_steps)
        return np.meshgrid(x, y, indexing='xy')

    @property
    def x_mesh(self):
        return self.get_matrix()[0]

    @property
    def y_mesh(self):
        return self.get_matrix()[1]

    @property
    def x_range(self):
        """
        x range of simulation in (start, end) in mm.
        :return: (start, end) of x in mm
        """
        return self._x_range

    @x_range.setter
    def x_range(self, value):
        try:
            assert len(value) == 2
        except (AssertionError, ValueError, TypeError, IndexError):
            raise ValueError("Mesh: (x1, x2) expected for x range.")
        self._x_range = value

    @property
    def x_step(self):
        """
        Step length computed from x range and steps.
        :return: float, in mm.
        """
        return (self.x_range[1] - self.x_range[0]) / (self.x_steps - 1)

    @property
    def y_step(self):
        """
        Step length computed from y range and steps.
        :return: float, in mm.
        """
        return (self.y_range[1] - self.y_range[0]) / (self.y_steps - 1)

    @property
    def x_linspace(self):
        return np.linspace(self.x_range[0], self.x_range[1], self.x_steps)

    @property
    def y_linspace(self):
        return np.linspace(self.y_range[0], self.y_range[1], self.y_steps)

    @property
    def pixel_bounds(self):
        """
        Returns the pixel boundary coordinates for matplotlib.pcolor:
        :return: [(m+1, n+1), (m+1, n+1)] shaped arrays.
        """
        x_step = self.x_step
        y_step = self.y_step
        x_start = self.x_range[0] - x_step / 2
        x_end = self.x_range[1] + x_step / 2
        y_start = self.y_range[0] - y_step / 2
        y_end = self.y_range[1] + y_step / 2
        x = np.linspace(x_start, x_end, self.x_steps + 1)
        y = np.linspace(y_start, y_end, self.y_steps + 1)
        return np.meshgrid(x, y)

    @property
    def x_pixel_bounds(self):
        """
        see pixel_bounds but only for x
        :return: (m, n) array
        """
        return self.pixel_bounds[0]

    @property
    def y_pixel_bounds(self):
        """
        see pixel_bounds but only for y
        :return: (m, n) array
        """
        return self.pixel_bounds[1]


def _slice_list(entries, processes=4):
    count = len(entries)
    per_proc = count // processes
    # extra = count % processes
    output = []
    ptr = 0
    for i in range(0, processes):
        if i < processes:
            output.append(entries[ptr: ptr + per_proc + 1])
            ptr = ptr + per_proc + 1
        else:
            output.append(entries[ptr: ptr + per_proc])
            ptr = ptr + per_proc
    return output


class Task(object):
    def __init__(self, sources=None, mesh=None):
        self.done = False
        self._sources = []
        self._mesh = None
        self._x_field = None
        self._y_field = None
        self._center_field = None
        self._x_field_interpolator = None
        self._y_field_interpolator = None
        if sources is not None:
            try:
                for source in sources:
                    self.add_source(source)
            except TypeError:
                self.add_source(sources)

        if mesh is not None:
            self.set_mesh(mesh)

    def add_source(self, magnet):
        if isinstance(magnet, CurrentLoop):
            self._sources.append(magnet.__copy__())
            self.done = False
        else:
            raise TypeError("Add magnet: Wrong type supplied, expected magnet definition.")

    def remove_source(self, index: (int, None) = None):
        """
        Remove magnet at index n.
        :param index: index to be removed. Clears the list if not provided.
        :return: None
        """
        if index is None:
            self._sources = []
        else:
            self._sources.pop(index)

    def set_mesh(self, mesh: Mesh):
        """
        Sets the mesh of this calculation.
        :param mesh: Mesh object.
        :return: None
        """
        if isinstance(mesh, Mesh):
            self._mesh = mesh
            self.done = False
        else:
            raise TypeError("Set mesh: Wrong type supplied: expected mesh.")

    def run(self, processes: int = 1):
        """
        User-facing wrapper for single-process and multi-process run methods.
        :param processes: Number of processes: 1 for single-threaded
        :return: None
        """
        if processes < 1:
            raise ValueError("Task run: number of processes cannot be smaller than 1")
        if processes == 1:
            self._run_sp()
        else:
            if multiprocessing is not None:
                self._run_mp(processes=processes)
            else:
                logger.log_event("Multiprocessing module disabled - falling back to single-threaded calculation")
                self._run_sp()

    def _run_sp_legacy(self):
        """
        Single-threaded solver without vectorization, slow for larger meshes or magnets.
        :return: None
        """
        if self.done:
            return
        x_mesh, y_mesh = self._mesh.get_matrix()
        x_field = np.zeros(x_mesh.shape)
        y_field = np.zeros(x_mesh.shape)
        for i in range(x_mesh.shape[0]):
            for j in range(x_mesh.shape[1]):
                for magnet in self._sources:
                    loops = magnet.get_loop_list()
                    for loop in loops:
                        xp = x_mesh[i][j]
                        yp = y_mesh[i][j]
                        a = loop[1] / 1000
                        x = (xp - loop[0]) / 1000
                        r = yp / 1000
                        current = loop[2]
                        bx = loop_calculator.field_axial(current, a, x, r)
                        br = loop_calculator.field_radial(current, a, x, r)
                        x_field[i][j] += bx
                        if r >= 0:
                            y_field[i][j] += br
                        else:
                            y_field[i][j] -= br
        self.done = True
        self._x_field = x_field
        self._y_field = y_field
        self._x_field_interpolator, self._y_field_interpolator = self._make_field_interpolator()
        self._center_field = self.calculate_center_field()

    def _run_sp(self):
        logger.clear_timer(1)
        if self.done:
            return
        x_mesh, y_mesh = self._mesh.get_matrix()
        x_field = np.zeros(x_mesh.shape)
        y_field = np.zeros(x_mesh.shape)
        loops = np.vstack([magnet.get_loop_list() for magnet in self._sources])
        for i in range(x_mesh.shape[0]):
            for j in range(x_mesh.shape[1]):
                xp = x_mesh[i][j]
                yp = y_mesh[i][j]
                a = loops[:, 1] / 1000
                x = (xp - loops[:, 0]) / 1000
                r = yp / 1000
                current = loops[:, 2]
                bx = loop_calculator.field_axial(current, a, x, r)
                br = loop_calculator.field_radial(current, a, x, r)
                x_field[i][j] += np.sum(bx)
                if r >= 0:
                    y_field[i][j] += np.sum(br)
                else:
                    y_field[i][j] -= np.sum(br)
        self.done = True
        logger.timestamp(1, "SP run complete")
        self._x_field = x_field
        self._y_field = y_field
        self._x_field_interpolator, self._y_field_interpolator = self._make_field_interpolator()
        self._center_field = self.calculate_center_field()

    @staticmethod
    def _mp_process_run(ij_list, x_mesh, y_mesh, loop_list):
        x_field = np.zeros(x_mesh.shape)
        y_field = np.zeros(x_mesh.shape)
        loops = np.asarray(loop_list)
        for i, j in ij_list:
            xp = x_mesh[i][j]
            yp = y_mesh[i][j]
            a = loops[:, 1] / 1000
            x = (xp - loops[:, 0]) / 1000
            r = yp / 1000
            current = loops[:, 2]
            bx = loop_calculator.field_axial(current, a, x, r)
            br = loop_calculator.field_radial(current, a, x, r)
            x_field[i][j] += np.sum(bx)
            if r >= 0:
                y_field[i][j] += np.sum(br)
            else:
                y_field[i][j] -= np.sum(br)
        return x_field, y_field

    def _run_mp(self, processes):
        logger.clear_timer(0)
        if self.done:
            return
        x_mesh, y_mesh = self._mesh.get_matrix()
        x_field = np.zeros(x_mesh.shape)
        y_field = np.zeros(x_mesh.shape)
        i = range(0, x_mesh.shape[0])
        j = range(0, x_mesh.shape[1])
        magnet_loops = np.vstack([magnet.get_loop_list() for magnet in self._sources])
        split_ij = _slice_list(list(product(i, j)), processes)
        logger.timestamp(0, "Slicing done")
        pool = multiprocessing.Pool(processes=processes)
        logger.timestamp(0, "processes spawned")
        argliist = [[x, x_mesh, y_mesh, magnet_loops] for x in split_ij]
        results = pool.starmap(self._mp_process_run, argliist)
        logger.timestamp(0, "pool closed")
        for result in results:
            x_field += result[0]
            y_field += result[1]

        self.done = True
        self._x_field = x_field
        self._y_field = y_field
        self._x_field_interpolator, self._y_field_interpolator = self._make_field_interpolator()
        self._center_field = self.calculate_center_field()
        logger.timestamp(0, "all done")

    def calculate_center_field(self, xc=0, yc=0):
        fx = self.x_field_at([xc, yc])
        fy = self.y_field_at([xc, yc])
        return fx, fy

    @property
    def magnets(self):
        return self._sources

    @property
    def x_field(self):
        """
        Axial magnetic field.
        :return: (m, n) array
        """
        if not self.done:
            raise ValueError("field not solved yet.")
        else:
            return self._x_field

    @property
    def y_field(self):
        """
        Radial magnetic field.
        :return: (m, n) array
        """
        if not self.done:
            raise ValueError("field not solved yet.")
        else:
            return self._y_field

    @property
    def mesh(self):
        """
        Mesh object used in calculation
        :return: Mesh object
        """
        if self._mesh is None:
            raise ValueError("Mesh not yet set.")
        else:
            return self._mesh

    @property
    def x_mesh(self):
        if self._mesh is None:
            raise ValueError("Mesh not yet set.")
        else:
            return self._mesh.x_mesh

    @property
    def y_mesh(self):
        if self._mesh is None:
            raise ValueError("Mesh not yet set.")
        else:
            return self._mesh.y_mesh

    @property
    def x_pixel_bounds(self):
        if self._mesh is None:
            raise ValueError("Mesh not yet set.")
        else:
            return self._mesh.x_pixel_bounds

    @property
    def y_pixel_bounds(self):
        if self._mesh is None:
            raise ValueError("Mesh not yet set.")
        else:
            return self._mesh.y_pixel_bounds

    @property
    def center_field(self):
        if not self.done:
            raise ValueError("field not solved yet.")
        else:
            return self._center_field

    @property
    def x_field_at(self):
        return self._x_field_interpolator

    @property
    def y_field_at(self):
        return self._y_field_interpolator

    def _make_field_interpolator(self):
        x = self.mesh.x_linspace
        y = self.mesh.y_linspace
        xi = RegularGridInterpolator((x, y), self._x_field.T)
        yi = RegularGridInterpolator((x, y), self._y_field.T)

        return xi, yi

    def make_gradient_interpolator(self, lat_field_axis='y', gradient_axes="xyt"):
        # TODO: figure out if RegularGridInterpolator REALLY takes ij indexing instead of xy
        g = find_gradient(self, lat_field_axis=lat_field_axis, gradient_axes=gradient_axes)
        x = self.mesh.x_linspace
        y = self.mesh.y_linspace
        # x = self.x_mesh.ravel()
        # y = self.y_mesh.ravel()
        # return LinearNDInterpolator((x, y), g.ravel())
        return RegularGridInterpolator((x, y), g.T)


def run_task(mesh: Mesh, sources: [CurrentLoop], processes=1):
    """
    Takes a mesh and a list of magnets and run the simulation.
    :param mesh: Mesh.
    :param sources: A list of Magnets.
    :param processes: Number of parallel processes.
    :return: the finished calculation object.
    """
    cal = Task(mesh=mesh, sources=sources)
    cal.run(processes=processes)
    return cal


def run_magnets_on_mesh(mesh, sources_list, processes=1):
    """
    Run multiple sets of magnets on the mesh, supports multiprocessing.
    :param mesh: Mesh to be used in calculations.
    :param sources_list: a LIST of LISTS of magnets, like:
    [[mag1_1, mag1_2, mag1_3],
     [mag2_2, mag2_2, mag2_3],
     ...]
    :param processes: Number of parallel processes to run.
    :return: A list of finished Tasks.
    """
    if multiprocessing is None and processes > 1:
        print("multiprocessing not working, falling back to single threaded operation")
        result = []
        for magnets in sources_list:
            task = Task(mesh=mesh, sources=magnets)
            task.run()
            result.append(task)
        return result
    else:
        pool = multiprocessing.Pool(processes=processes)
        arglist = [[mesh, magnets] for magnets in sources_list]
        return pool.starmap(run_task, arglist)


def _run_this(task):
    task.run()
    return task


def run_tasks(tasks: [Task], processes=1):
    """
    Runs every task in a list of tasks, returns done list of done tasks.
    The original list of tasks REMAINS UNTOUCHED!
    :param tasks: list of tasks
    :param processes: number of processes
    :return: list of tasks(done)
    """
    if multiprocessing is None and processes > 1:
        print("multiprocessing not working, falling back to single threaded calculation")
        for task in tasks:
            task.run()
        return tasks
    else:
        pool = multiprocessing.Pool(processes=processes)
        return pool.map(_run_this, tasks)
