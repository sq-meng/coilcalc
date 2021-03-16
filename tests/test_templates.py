import coilcalc
from coilcalc import templates


def test_comp_solenoid():
    templates.compensated_solenoid()
    templates.helmholtz_coil()
    templates.three_coils()
