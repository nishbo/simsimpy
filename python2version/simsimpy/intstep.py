from itertools import izip

def euler(prev, right_side, t, dt):
    return [p + dt*r for p, r in izip(prev, right_side(t, *prev))]
    # return prev + dt*right_side(t, *prev)


def rk4(prev, right_side, t, dt):
    """ right_side = right_side(t, *(y))
        right_side: R^(t+len(prev)) -> R^len(prev)
        right side MUST return an array
    """
    k1 = right_side(t, *prev)
    k2 = right_side(t+dt/2, *[pi+dt*k1i/2 for pi, k1i in izip(prev, k1)])
    k3 = right_side(t+dt/2, *[pi+dt*k2i/2 for pi, k2i in izip(prev, k2)])
    k4 = right_side(t+dt, *[pi+dt*k3i for pi, k3i in izip(prev, k3)])
    return [pi + dt/6*(k1i+2*k2i+2*k3i+k4i)
            for pi, k1i, k2i, k3i, k4i in izip(prev, k1, k2, k3, k4)]
