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
        def get_size(h, w, _): return width, int(h * width / w)
    elif width is None:
        def get_size(h, w, _): return int(w * height / h), height
    else:
        def get_size(h, w, _): return w, h

    def apply(img: NDArray):
        img = misc.D3(img)
        size = get_size(*img.shape)
        # Do resize
        img = types.U8(img)
        return np.squeeze(cv2.resize(img, size))
    return apply
