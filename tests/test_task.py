import coilcalc
import pytest
import coilcalc.calculations
import numpy as np


@pytest.fixture
def task():
    class TaskFactory(object):
        def get(self):
            mesh = coilcalc.Mesh([-20, 20], [-10, 10], 21, 21)
            mytask = coilcalc.Task()
            mag1 = coilcalc.CurrentLoop([-50, 50], [20, 20], 21, 1.2, 4)
            mag2 = coilcalc.CurrentLoop([-50, -40], [20, 20], 5, 1.2, 1)
            mytask.set_mesh(mesh)
            mytask.add_source(mag1)
            mytask.add_source(mag2)
            return mytask
    return TaskFactory()


def test_task_run(task):
    t1 = task.get()
    with pytest.raises(ValueError):
        _ = t1.x_field
    t1._run_sp_legacy()
    _ = t1.x_field
    coilcalc.calculations.find_gradient(t1)
    with pytest.raises(ValueError):
        coilcalc.calculations.fom_cylindrical_cell(t1, 30, 25)
    coilcalc.calculations.fom_cylindrical_cell(t1, 30, 15)


def test_task_slicer():
    pass


def test_mp_sp(task):
    task1 = task.get()
    task2 = task.get()
    task3 = task.get()

    assert task1 is not task2
    assert task2 is not task3

    task1._run_mp(processes=4)
    assert task1.done
    assert not task2.done
    task2._run_sp()
    task3._run_sp_legacy()

    assert np.all(np.isclose(task1.x_field, task3.x_field))
    assert np.all(np.isclose(task1.y_field, task3.y_field))
    assert np.all(np.isclose(task2.x_field, task3.x_field))
    assert np.all(np.isclose(task2.y_field, task3.y_field))


def test_run_tasks_mp(task):
    tasks = [task.get(), task.get(), task.get()]
    tasks = coilcalc.run_tasks(tasks, processes=2)
    assert ([x.done for x in tasks])


def test_run_tasks_sp(task):
    tasks = [task.get(), task.get(), task.get()]
    tasks = coilcalc.run_tasks(tasks, processes=1)
    assert ([x.done for x in tasks])
