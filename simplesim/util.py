import time


def timeit(fn):
    a = time.perf_counter_ns()
    fn()
    b = time.perf_counter_ns()
    dx = (b - a) * 1e-9
    return "%.3g" % (dx)


def sign_int(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0