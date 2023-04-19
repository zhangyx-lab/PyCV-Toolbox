# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from ..__internal__ import *
from .. import types
from .__interactive__ import Interactive
# --------------------------------------------------

class Layout(Interactive):
    padding = (0, 0, 0, 0)

    def rasterize(self):
        raise NotImplementedError

class GridLayout(Layout):
    def __init__(self, *grid, cols=None, rows=None, padding=0, margin=0, gridSize=(100, 100), whiteSpaceColor=(0,0,0)):
        pass