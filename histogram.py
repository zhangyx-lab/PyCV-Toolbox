# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import types, fx
# --------------------------------------------------


def histo(img: NDArray, bins=[]):
    pass


def dynamic(*percentiles: float):
    """
    (lambda) reports the brightness at given percentile(s)
    """
    # Ensure percentiles are legal
    for p in percentiles:
        assert p >= 0 and p <= 1, f"Percentile {p} out of range(0, 1)"

    def apply(img: NDArray) -> list[float]:
        nonlocal percentiles
        # Ensure dtype is float[any]
        img = types.to_float(img)
        # Convert image to 1D array
        arr = img.reshape((-1,))
        # Sort the flattened image
        arr.sort()
        # Convert float position to array indexes
        i_max = len(arr) - 1
        indexes = [int(p * i_max) for p in percentiles]
        # Return result
        return [arr[i] for i in indexes]
    return apply


def contrast(c: float, fit=None):
    """
    (Lambda) Adjust given image by given contrast,
    contrast should be a positive float value.
    """
    assert c > 0, f"contrast {c} should be positive"
    if fit is None:
        fit = types.trimToFit

    def apply(img: NDArray):
        nonlocal c, fit
        img = fit(types.to_float(img))
        img = fx.project(dst=[-1, 1])(img)
        # Do contrast adjustment
        mask = img < 0
        img = np.absolute(img)
        img = img ** (1 / c)
        img[mask] *= -1
        # Convert back to 0-1 dynamic range
        img = fx.project(src=[-1, 1])(img)
        return img
    return apply


def gamma(g: float = None, reference: NDArray | float = None):
    """
    (Lambda) Adjust given image by given gamma,
    gamma should be a positive float value.
    If g is not given, it will default to match the reference.
    If both g and reference are missing, it will align to 0.5.
    """
    def apply(img: NDArray):
        nonlocal g, reference
        img = types.to_float(img)
        img = types.trimToFit(img)
        if g is None:
            src = np.average(img)
            if reference is None:
                dst = 0.5
            elif isinstance(reference, np.ndarray):
                dst = types.to_float(reference)
                dst = types.trimToFit(dst)
                dst = np.average(dst)
            else:
                assert isinstance(reference, float) or isinstance(reference, int), reference
                dst = float(reference)
            g = math.log(dst) / math.log(src)
        # Run gamma correction
        return img ** g
    return apply
