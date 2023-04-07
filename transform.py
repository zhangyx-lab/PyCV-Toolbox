# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import types, misc
# --------------------------------------------------


def resize(height: int = None, width: int = None):
    """
    (Lambda) Will resize the image to given height of width
    """
    if height is None:
        assert width is not None
        def get_size(h, w, _): return int(h * width / w), width
    elif width is None:
        def get_size(h, w, _): return height, int(w * height / h)
    else:
        def get_size(h, w, _): return h, w

    def apply(img: NDArray):
        img = misc.D3(img)
        size = get_size(*img.shape)
        # Do resize
        img = types.U8(img)
        return np.squeeze(cv2.resize(img, size))
    return apply
