# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import types, fx
# --------------------------------------------------


def gray(weights=None, bands: list[float | int] = None):
    def apply(img: NDArray) -> np.floating:
        img = types.to_float(img)
        nonlocal weights, bands
        if img.ndim < 3:
            return img
        assert img.ndim == 3, img.shape
        if bands is None:
            bands = np.array(range(img.shape[2]))
        if callable(weights):
            weights = weights(bands)
        if isinstance(weights, np.ndarray):
            weights = weights.astype(np.float32)
            weights /= np.sum(weights)
        return np.average(img, axis=2, weights=weights)
    return apply


def invert(rgb):
    if not isinstance(rgb, np.ndarray):
        rgb = np.ndarray(rgb)
    if isinstance(rgb, np.floating):
        return 1 - rgb
    else:
        assert isinstance(rgb, np.unsignedinteger), rgb.dtype
        return types._dtype_max(rgb.dtye) - rgb


def wave2bgr(wave: float, invisible=0.3):
    B = fx.project(src=(510, 490))(wave)
    G = np.min([fx.project(src=(440, 490))(wave),
               fx.project(src=(645, 580))(wave)])
    R = np.max([fx.project(src=(440, 380))(wave),
               fx.project(src=(510, 580))(wave)])
    intensity = np.max([
        np.min([
            fx.project(src=(380, 420))(wave),
            fx.project(src=(780, 700))(wave)
        ]),
        invisible
    ])
    color = types.trimToFit(types.to_float([B, G, R]))
    color = fx.gamma(0.8)(color * intensity)
    return types.trimToFit(color)
