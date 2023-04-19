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

    def main_loop(self, waitKeyDuration=0):
        user_key = cv2.waitKey(waitKeyDuration)
        for window in self.windows:
            window.onKey(user_key)
        return user_key
