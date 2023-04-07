# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
# --------------------------------------------------


def gamma(g: float):
    def apply(x: NDArray | int | float):
        return x ** g
    return apply


def project(src=[0, 1], dst=[0, 1]):
    """Project a scalar or array value from one given range to another"""
    # Check for zero-width projection ranges
    assert src[0] != src[1], src
    assert dst[0] != dst[1], dst

    def apply(value: NDArray | float | int):
        # Caculate projection scale ratio
        rs, rd = [r - l for l, r in (src, dst)]
        ratio = rd / rs
        # Align value with src[0]
        return (value - src[0]) * ratio + dst[0]
    return apply


def gaussian(mu=0, sigma=1):
    return lambda x: np.exp(-np.square((x - mu) / (sigma ** 2)))
