def range_generate_regenerate(gen, mi, ma):
    if mi == ma:
        return mi
    ans = gen()
    while ans > ma or ans < mi:
        ans = gen()
    return ans


def range_generate_doborder(gen, mi, ma):
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
