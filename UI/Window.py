# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from ..__internal__ import *
from .. import types
from ._interactive_ import KeyboardInteractive, MouseInteractive
from .Layout import Layout
# --------------------------------------------------


class Window(KeyboardInteractive, MouseInteractive):
    flags = [
        (cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE),
        (cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    ]
    def __init__(self, name, content: Layout, *flags: tuple[int, int]):
        super().__init__()
        self.name = name
        self.flags += list(flags)

    def __enter__(self):
        # Declare window instance
        cv2.namedWindow(self.name)
        # Set window flags
        for propId, value in self.flags:
            cv2.setWindowProperty(self.name, propId, value)
        # Register mouse handler callback
        self.__handle_mouse__(self.name)

    def __exit__(self, *exc_details):
        cv2.destroyWindow(self.name)

    def render(self):
        cv2.imshow(self.name, self.content.rasterize())

class Session(KeyboardInteractive):
    def __init__(self, *windows: Window):
        self.windows = windows

    def __enter__(self):
        for window in self.windows:
            window.__enter__()
            return self

    def __exit__(self, errType, err, trace):
        for window in self.windows:
            window.__exit__()
