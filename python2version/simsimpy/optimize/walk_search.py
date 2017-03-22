import numpy
from ..other import dlogrange
from scipy.optimize import OptimizeResult


def generate_all_directions(length, root=True):
    """Generates all possible directions for movement in length-dimentional
    space.

    Includes the diagonal points. Usually is less efficient than
        generate_nondiagonal_directions
    """
    if length < 1:
        return [[]]
    else:
        a = generate_all_directions(length - 1, root=False)
        answ = []
        for i in a:
            answ.append(list(i) + [-1])
            answ.append(list(i) + [0])
            answ.append(list(i) + [1])
        if root:
            answ.pop(answ.index([0]*length))
        return answ


def generate_nondiagonal_directions(length):
    """Generates all possible directions for movement in length-dimentional
    space.

    Each vector has only one non-zero element, which eq to -1 or 1.
    """
    answ = []
    for i in xrange(length):
        answ.append([0]*length)
        answ.append([0]*length)

        answ[-1][i] = -1
        answ[-2][i] = 1
    return answ


def test_nearby_points(target, point, dx, diagonal=False):
    """Tests if any nearby points are bigger than the point.

    dx is a scalar
    Returns set of directions and a list of function values.
    """
    point = numpy.array(point)

    if diagonal:
        directions = generate_all_directions(len(point))
    else:
        directions = generate_nondiagonal_directions(len(point))

    res = []
    for direction in directions:
        res.append(target(point + direction*dx))

    return [directions, res]


def _res_around(target, x0, dx, directions, bounds):
    """Calculates function values around the point from a set of directions."""
    res = []
    for direction in directions:
        x = x0 + direction*dx
        if bounds is None or bounds(x_new=x):
            res.append(target(x))
        else:
            res.append(numpy.inf)
    return res


def walk(target, x0, dx, directions, bounds=None, ytol_rel=1e-7):
    """A simple gradient walk search, that moves point according to dx until
    ytol_rel is met or the minimum is found.

    Suggest using the scipy wrap version. Use _generate_*_directions functions
    to create direction functions.

    parameters:
        target: function to be minimized
        x0: starting point
        dx: scalar step in directions
        directions: list of lists with all possible direction for point
            movement. See generate_directions functions for more info.
        bounds: a function that evaluates if x is within bounds
        ytol_rel: search is stopped when 1. - new_min/old_min < ytol_rel. Used
            to cut some long slopes. Set to negative to remove.
    returns:
        x0: point of minimum
        fval: value of target in minimum
        fnval: amount of function evaluations
    """
    fval = target(x0)
    res = _res_around(target, x0, dx, directions, bounds)
    fnval = len(directions) + 1
    while 1. - min(res) / fval > ytol_rel:
        # update
        x0 += directions[res.index(min(res))]*dx
        fval = target(x0)
        # calc nearby
        res = _res_around(target, x0, dx, directions, bounds)
        fnval += len(directions)
    return {'x0': x0, 'fval': fval, 'fnval': fnval}


def graduate_walk(target, x0, dx, directions, dx_start, dx_step, bounds=None,
                  ytol_rel=1e-7):
    """A simple gradient walk search, that moves point according to dx until
    ytol_rel is met or the minimum is found.

    dx step is changing for faster descend. Function will go through all
        ddx = dx_start * dx_step ** i
    until dx is reached.

    Suggest using the scipy wrap version. Use _generate_*_directions functions
    to create direction functions.

    parameters:
        target: function to be minimized
        x0: starting point
        dx: scalar step in directions
        directions: list of lists with all possible directions for point
            movement. See generate_directions functions for more info.
        dx_start: starting value for dx step. Must be bigger that dx.
        dx_step: change of dx on each iteration. Should be less than 1.
        bounds: a function that evaluates if x is within bounds
        ytol_rel: search is stopped when 1. - new_min/old_min < ytol_rel. Used
            to cut some long slopes. Set to negative to remove.
    returns:
        x0: point of minimum
        fval: value of target in minimum
        fnval: amount of function evaluations
    """
    fnval = 0
    if dx_start < dx or dx_step >= 1 or dx < 0:
        raise Exception('dx, dx_start or dx_step were set incorrectly.')
    dxs = list(dlogrange(dx_start, dx_step, stop=dx))
    if dx not in dxs:
        dxs.append(dx)
    for ddx in dxs:
        res = walk(target, x0, ddx, directions, bounds=bounds,
                   ytol_rel=ytol_rel)
        x0 = res['x0']
        fnval += res['fnval']

    return {'x0': x0, 'fval': res['fval'], 'fnval': fnval}


def scipy_walk(*args, **kwargs):
    """Scipy-compatible walk function wrapper.

    parameters:
        args[0]: target, function to be minimized
        args[1]: x0, starting point for minimization
        dx=1e-8: step in change of the point
        diagonal=False: defines directions for point movements. See
                generate_all_directions
                generate_nondiagonal_directions
            for more information.
        bounds=None: list of bounds for the movement
                [[min, max], [min, max], ...]
            if set to None, bounds are ignored
        ytol=1e-8: relative tolerance for search stop. See walk for more info.
    returns:
        OptimizeResult() object with properly set x, fun, nfev.
            success is always set to True, status to 1
    """
    target = args[0]
    x0 = args[1]
    dx = kwargs['dx'] if 'dx' in kwargs.keys() else 1e-8
    if 'diagonal' in kwargs.keys() and kwargs['diagonal']:
        directions = generate_all_directions(len(x0))
    else:
        directions = generate_nondiagonal_directions(len(x0))
    if 'bounds' in kwargs.keys() and kwargs['bounds'] is not None:
        bounds = Bounds(kwargs['bounds'])
    else:
        bounds = None
    ytol_rel = kwargs['ytol_rel'] if 'ytol_rel' in kwargs.keys() else 1e-8

    res = walk(target, x0, dx, directions, bounds=bounds, ytol_rel=ytol_rel)

    answ = OptimizeResult()
    answ.x = res['x0']
    answ.fun = res['fval']
    answ.success = True
    answ.status = 1
    answ.nfev = res['fnval']
    return answ


def scipy_graduate_walk(*args, **kwargs):
    """Scipy-compatible graduate_walk function wrapper.

    parameters:
        args[0]: target, function to be minimized
        args[1]: x0, starting point for minimization
        dx=1e-8: step in change of the point
        dx_start=0.1: starting value for dx step. Must be bigger that dx.
        dx_step=0.1: change of dx on each iteration. Should be less than 1.
        diagonal=False: defines directions for point movements. See
                generate_all_directions
                generate_nondiagonal_directions
            for more information.
        bounds=None: list of bounds for the movement
                [[min, max], [min, max], ...]
            if set to None, bounds are ignored
        ytol=1e-8: relative tolerance for search stop. See graduate_walk for
            more info.
    returns:
        OptimizeResult() object with properly set x, fun, nfev.
            success is always set to True, status to 1
    """
    target = args[0]
    x0 = args[1]
    dx = kwargs['dx'] if 'dx' in kwargs.keys() else 1e-8
    dx_start = kwargs['dx_start'] if 'dx_start' in kwargs.keys() else 0.1
    dx_step = kwargs['dx_step'] if 'dx_step' in kwargs.keys() else 0.1
    if 'diagonal' in kwargs.keys() and kwargs['diagonal']:
        directions = generate_all_directions(len(x0))
    else:
        directions = generate_nondiagonal_directions(len(x0))
    if 'bounds' in kwargs.keys() and kwargs['bounds'] is not None:
        bounds = Bounds(kwargs['bounds'])
    else:
        bounds = None
    ytol_rel = kwargs['ytol_rel'] if 'ytol_rel' in kwargs.keys() else 1e-8

    res = graduate_walk(target, x0, dx, directions, dx_start, dx_step,
                        bounds=bounds, ytol_rel=ytol_rel)

    answ = OptimizeResult()
    answ.x = res['x0']
    answ.fun = res['fval']
    answ.success = True
    answ.status = 1
    answ.nfev = res['fnval']
    return answ
