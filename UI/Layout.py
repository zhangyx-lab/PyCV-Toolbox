# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from ..__internal__ import *
from .. import types
from ._interactive_ import KeyboardInteractive, MouseInteractive
# --------------------------------------------------
# Layout of a window splits the window into multiple
# regions, each region can be assigned to a layout or
# content producer.
def param_4d(*args, typecheck=None) -> tuple:
    """
    Four parameters are required to specify a rectangle:

    +  0  +
    3     1
    +  2  +

    """
    # Check for input argument type
    if typecheck is not None:
        if not all(isinstance(arg, typecheck) for arg in args):
            ValueError(f"Invalid parameter: {args}")
    # Check for input argument count
    if len(args) == 1:
        args = list(args) * 4
    elif len(args) == 2:
        args = list(args) * 2
    elif len(args) != 4:
        raise ValueError(f"Invalid parameter set: {args}")
    # Return normailzed parameters
    return tuple(args)

class Layout(KeyboardInteractive, MouseInteractive):
    def rasterize(self) -> NDArray:
        raise NotImplementedError
    
class PlainContentLayout(Layout):
    def __init__(self, content: NDArray):
        self.content = types.U8(content)

    def rasterize(self):
        return self.content

class PaddedCellLayout(Layout):
    padding: tuple[int, int, int, int] = None
    def __init__(self, content: Layout, *padding: int, color=(0,0,0)):
        self.content = content
        self.padding = param_4d(*padding, typecheck=int)
        self.color = color

    def rasterize(self):
        top, right, bottom, left = self.padding
        return cv2.copyMakeBorder(self.content.rasterize(), top, bottom, left, right, cv2.BORDER_CONSTANT, value=self.color)

class GridLayout(Layout):
    def __init__(self, *grid, cols=None, rows=None, padding=0, margin=0, gridSize=(100, 100), whiteSpaceColor=(0,0,0)):
        pass
