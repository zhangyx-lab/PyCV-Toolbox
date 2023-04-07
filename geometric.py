# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import types, misc, spectral, histogram
# --------------------------------------------------


def equalize(kernelSize: int = None) -> np.floating:
    if kernelSize is None:
        return types.to_float
    assert kernelSize % 2 == 1, "kernel size for equalization must be an ODD integer"

    def apply(cube: NDArray):
        # Convert cube to float with range 0 - 1
        cube = types.to_float(cube)
        # Flatten the image into grayscale => ndim = 2
        flat = spectral.gray()(cube)
        # Compute the overall brightness channel
        level = np.average(flat)
        # Compute local brightness distribution
        local = cv2.GaussianBlur(flat, [kernelSize] * 2, 0)
        # Compute the scale ration for each pixel
        scale = level / local
        scale = scale / np.average(scale)
        # Broadcast operands
        if cube.ndim == 3: scale = misc.D3(scale)
        # Apply scale
        cube *= scale
        # Limit the value range within 0-1
        return types.trimToFit(cube)
    return apply
