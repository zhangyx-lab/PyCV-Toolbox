# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from ..__internal__ import *
from .. import types
from .__interactive__ import Interactive
# --------------------------------------------------


class Window(Interactive):

    def __init__(self, name, flags=cv2.WINDOW_AUTOSIZE):
        super().__init__()
        self.name = name
        self.win_flags = flags

    def __enter__(self):
        # Declare window instance
        cv2.namedWindow(self.name)
        # Register callback
        super().registerMouseCallback(self.name)

    def __exit__(self, *exc_details):
        cv2.destroyWindow(self.name)

    def render(self, img: NDArray):
        cv2.imshow(self.name, types.U8(img))
