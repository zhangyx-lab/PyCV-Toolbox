# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from ..__internal__ import *
from .. import types
from . import Window
# --------------------------------------------------


class Session:
    def __init__(self, *windows: Window):
        self.windows = windows

    def __enter__(self):
        for window in self.windows:
            window.__enter__()
            return self

    def __exit__(self, errType, err, trace):
        for window in self.windows:
            window.__enter__()
