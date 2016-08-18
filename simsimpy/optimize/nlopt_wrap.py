from scipy.optimize import OptimizeResult
try:
    import nlopt
except:
    nlopt = None


def scipy_nlopt_cobyla(*args, **kwargs):
    """Wraps nlopt library cobyla function to be compatible with scipy optimize

    parameters:
        args[0]: target, function to be minimized
        args[1]: x0, starting point for minimization
        bounds: list of bounds for the movement
                [[min, max], [min, max], ...]
        ftol_rel: same as in nlopt
        xtol_rel: same as in nlopt
            one of the tol_rel should be specified
    returns:
        OptimizeResult() object with properly set x, fun, success.
            status is not set when nlopt.RoundoffLimited is raised
    """
    answ = OptimizeResult()
    bounds = kwargs['bounds']

    opt = nlopt.opt(nlopt.LN_COBYLA, len(args[1]))
    opt.set_lower_bounds([i[0] for i in bounds])
    opt.set_upper_bounds([i[1] for i in bounds])
    if 'ftol_rel' in list(kwargs.keys()):
        opt.set_ftol_rel(kwargs['ftol_rel'])
    if 'xtol_rel' in list(kwargs.keys()):
        opt.set_ftol_rel(kwargs['xtol_rel'])
    opt.set_min_objective(args[0])

    x0 = list(args[1])

    try:
        x1 = opt.optimize(x0)
    except nlopt.RoundoffLimited:
        answ.x = x0
        answ.fun = args[0](x0)
        answ.success = False
        answ.message = 'nlopt.RoundoffLimited'
        return answ

    answ.x = x1
    answ.fun = args[0](x1)
    answ.success = True if opt.last_optimize_result() in [3, 4] else False
    answ.status = opt.last_optimize_result()
    if not answ.fun == opt.last_optimum_value():
        print('Something\'s wrong, ', answ.fun, opt.last_optimum_value())

    return answ
