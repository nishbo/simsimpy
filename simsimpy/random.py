def range_generate_regenerate(gen, mi, ma, cntr=None):
    """Uses gen to generate a random number inside [mi, ma].

    Random number is regenerated until it is inside [mi, ma] bounds. Counter
    could be specified to limit number of iterations. If the limit is reached,
    warning is raised and the border solution is returned.
    """
    if mi == ma:
        return mi
    ans = gen()
    if cntr is not None:
        i = 0
    while ans > ma or ans < mi:
        ans = gen()
        if cntr is not None:
            i += 1
            if i > cntr:
                ans = ma if ans > ma else mi
                break
    return ans


def range_generate_doborder(gen, mi, ma):
    """Uses gen to generate a random number inside [mi, ma].

    If it falls out of [mi, ma] bounds, it returns mi or ma, respectively.
    """
    ans = gen()
    if ans >= ma:
        return ma
    if ans <= mi:
        return mi
    return ans


def gamma_meanvariance_to_alphabeta(mean, variance):
    """Alpha-beta python style. E.g. k-theta wikipedia style."""
    return [variance/mean, mean*mean/variance]


def gamma_meansigma_to_alphabeta(mean, sigma):
    """Alpha-beta python style. E.g. k-theta wikipedia style."""
    return gamma_meanvariance_to_alphabeta(mean, sigma*sigma)
