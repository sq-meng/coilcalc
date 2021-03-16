import coilcalc


def test_mesh():
    mesh = coilcalc.Mesh([-50, 50], [-20, 20], 51, 21)
    assert tuple(mesh.x_range) == (-50, 50)
    assert mesh.x_step == 100 / 50
    assert mesh.y_step == 40 / 20
    assert mesh.x_pixel_bounds.shape == (22, 52)
    assert mesh.y_pixel_bounds.shape == (22, 52)


def test_pixel_boundaries():
    mesh = coilcalc.Mesh([-50, 50], [-20, 20], 51, 21)
    assert mesh.x_pixel_bounds[0][0] == -51
    assert mesh.x_pixel_bounds[0][51] == 51
    assert mesh.y_pixel_bounds[0][0] == -21
    assert mesh.y_pixel_bounds[21][51] == 21
