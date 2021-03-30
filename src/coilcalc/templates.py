from coilcalc.core import Magnet


def compensated_solenoid(length=300, d0=200, turns_main=420, turns_comp=63, wire_diameter=0.66, layers_main=1,
                         layers_comp=1, current=1):
    """
    Builds a solenoid with extra turns wound on top at both ends to compensate for the field lines "curving away"
    from axis. Achieves better field homogeneity with a small profile.
    :param length: Total length of coil.
    :param d0: Diameter of main coil.
    :param turns_main: Winding turns of the main solenoid without compensation coils.
    :param turns_comp: Winding turns of compensation coils at EACH end.
    :param wire_diameter: Enamel wire diameter used to calculate compensation coil diameter.
    :param layers_main: How many winding layers the main coil has. Usually 1 or 2.
    :param layers_comp: How many winding layers the compensation coil has.
    :param current: Current for the magnet - a single current flows all 3 coils.
    :return: A list of magnets.
    """
    mag_0 = Magnet([-length / 2, length / 2], d0 / 2, turns_main, current, layers_main, wire_diameter)
    mag_left = Magnet([-length / 2, -length / 2 + turns_comp * wire_diameter], d0 / 2 + wire_diameter, turns_comp,
                      current, layers_comp, wire_diameter)
    mag_right = Magnet([length / 2, length / 2 - turns_comp * wire_diameter], d0 / 2 + wire_diameter, turns_comp,
                       current, layers_comp, wire_diameter)
    return [mag_0, mag_left, mag_right]


def helmholtz_coil(r=300, coil_width=20.0, coil_thickness=5.0, current=1, turns=300):
    """
    Constructs a Helmholtz coil pair. Only 9 turns of current is actually simulated, with current scaled accordingly.
    :param r: Radius of coil.
    :param coil_width: Width of coil winding.
    :param coil_thickness: Thickness of coil winding.
    :param current: Current fed to coils.
    :param turns: Number of turns on each coil.
    :return: A list of magnets
    """
    dr = coil_width / 2
    mag_0 = Magnet([-r / 2 - dr, -r / 2 + dr], r - coil_thickness / 2, 9, current * turns / 9, 3, coil_thickness / 2)
    mag_1 = Magnet([r / 2 - dr, r / 2 + dr], r - coil_thickness / 2, 9, current * turns / 9, 3, coil_thickness / 2)

    return [mag_0, mag_1]


def three_coils(half_length=259.8, r_side=300, r_center=300, coil_width=20.0, coil_thickness=5.0, current=1, turns_side=300,
                turns_center=180):
    """
    Constructs a coil group with two identical side coils and one center coil with the same bobbin diameter.
    Each coil is simplified into 9 current loops to accelerate calculation.
    :param half_length: How far are side coils from center.
    :param r_side: Radius of side coils
    :param r_center: Radius of center coil.
    :param coil_width: Width of coil windings.
    :param coil_thickness: Thickness of coil windings.
    :param current: Current to be fed into the coils. All 3 coils have the same current.
    :param turns_side: Winding turns on the side coils.
    :param turns_center: Winding turns on the center coil.
    :return: A list of magnets
    """
    current_side_sim = current * turns_side / 9
    current_center_sim = current * turns_center / 9
    mag1 = Magnet([-half_length - coil_width / 2, -half_length + coil_width / 2], r_side, 9, current_side_sim, 3, coil_thickness / 2)
    mag2 = Magnet([half_length - coil_width / 2, half_length + coil_width / 2], r_side, 9, current_side_sim, 3, coil_thickness / 2)
    magc = Magnet([0 - coil_width / 2, 0 + coil_width / 2], r_center, 9, current_center_sim, 3, coil_thickness / 2)

    return [mag1, mag2, magc]


def maxwell_coil(r_center=300, coil_width=20.0, coil_thickness=5.0, current=1, turns_center=300):
    pass