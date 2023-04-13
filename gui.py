# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import types
# --------------------------------------------------

WINDOW_LIST = []

class Window:
    name = None
    def __init__(self, name):
        self.name = name

    def render(self, img: NDArray):
        cv2.imshow(self.name, types.U8(img))
    # Callback registerer
    onMouseMove = None
    onKeyPress = None

    @classmethod
    def mainLoop(cls):
        pass