import numpy


def brute(func, bounds, Ns, disp=False, *args, **kwargs):
    """Iterative implementation of brute-force optimization.

    Differs from scipy.optimize.brute implementation because is iterative and
    therefore does not eat that much memory. Is a little bit slower than scipy.
    Better for large memory-consuming tasks.

    parameters:
        func: The objective function to be minimized. func(x)
        bounds: [[min, max], [min, max], ...]
        Ns: amount of points per axis
        disp: if set to True, prints progress in a convenient progress line.
    returns:
        x0: A 1-D array containing the coordinates of a point at which the
        objective function had its minimum value.
        fval: Function value at the point x0.
    """
    [x, y] = _brute_rec(func, bounds, Ns, disp=disp)
    if disp:
        print()

    return {'x0': x, 'fval': y}


def _brute_rec(func, bounds, Ns, x_l=None, disp=False, disp_s=''):
    if x_l is None:
        x_l = []
    ys = []
    xs = []

    if len(bounds) == 1:
        for p_r in numpy.linspace(bounds[0][0], bounds[0][1], Ns):
            xs.append(x_l + [p_r])
            ys.append(func(xs[-1]))
        if disp:
            print(disp_s + '\r', end=' ')
        return [xs[ys.index(min(ys))], min(ys)]

    for i, p_r in enumerate(numpy.linspace(bounds[0][0], bounds[0][1], Ns)):
        x, y = _brute_rec(func, bounds[1:], Ns, x_l=x_l+[p_r], disp=disp,
                          disp_s=disp_s+'{:.2%} '.format(i/Ns))
        xs.append(x)
        ys.append(y)
    return [xs[ys.index(min(ys))], min(ys)]


def _f1(point, *params):
    x, y = point
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (a * x**2 + b * x * y + c * y**2 + d*x + e*y + f)


def _f2(point, *params):
    x, y = point
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (-g*numpy.exp(-((x-h)**2 + (y-i)**2) / scale))


def _f3(point, *params):
    x, y = point
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (-j*numpy.exp(-((x-k)**2 + (y-l)**2) / scale))


def _f(point, *params):
    return _f1(point, *params) + _f2(point, *params) + _f3(point, *params)


def _test():
    params = (2, 3, 7, 8, 9, 10, 44, -1, 2, 26, 1, -2, 0.5)
    func = lambda point: _f(point, *params)
    bounds = [(-4, 4)]*2
    print(brute(func, bounds=bounds, Ns=33))
    print('Scipy calc: point: array([-1.0 1.75]), fval: -2.892')


if __name__ == '__main__':
    _test()
