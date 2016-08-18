def euler(prev, right_side, t, dt):
    return prev + dt*right_side(t, *prev)


def rk4(prev, right_side, t, dt):
    """ right_side = right_side(t, *(y))
        right_side: R^(t+len(prev)) -> R^len(prev)
        right side MUST return an array
    """
    k1 = right_side(t, *prev)
    k2 = right_side(t+dt/2., *[prev[i]+k1[i]/2. for i in range(len(prev))])
    k3 = right_side(t+dt/2., *[prev[i]+k2[i]/2. for i in range(len(prev))])
    k4 = right_side(t+dt, *[prev[i]+k3[i] for i in range(len(prev))])
    return [prev[i] + dt/6.*(k1[i]+2.*k2[i]+2.*k3[i]+k4[i])
            for i in range(len(prev))]
