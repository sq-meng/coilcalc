import magcoilcalc
import numpy as np
import pytest


def test_source_collection():
    s1 = magcoilcalc.CurrentLoop([-50, 60], 50, 101, 2.0, 3, 1)
    s2 = magcoilcalc.CurrentSheet([-30, 40], 60, 101, 2.0)

    c1 = magcoilcalc.SourceCollection([s1, s2])
    c2 = magcoilcalc.SourceCollection(s1)
    c2.add_sources(s2)

    assert np.all(c1.b_field(10, 10) == c2.b_field(10, 10))
    assert np.all(
        np.array(c1.b_field(-20, 20)) == (np.array(s1.b_field(-20, 20)) + s2.b_field(-20, 20)))