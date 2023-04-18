# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from ..__internal__ import *
from .. import types
# --------------------------------------------------

# FLAG_ALTKEY
# FLAG_CTRLKEY
# FLAG_SHIFTKEY

# FLAG_LBUTTON
# FLAG_MBUTTON
# FLAG_RBUTTON

# None button events
MOUSEMOVE     = cv2.EVENT_MOUSEMOVE
MOUSEHWHEEL   = cv2.EVENT_MOUSEHWHEEL
MOUSEWHEEL    = cv2.EVENT_MOUSEWHEEL

LBUTTONDBLCLK = cv2.EVENT_LBUTTONDBLCLK
LBUTTONDOWN   = cv2.EVENT_LBUTTONDOWN
LBUTTONUP     = cv2.EVENT_LBUTTONUP

MBUTTONDBLCLK = cv2.EVENT_MBUTTONDBLCLK
MBUTTONDOWN   = cv2.EVENT_MBUTTONDOWN
MBUTTONUP     = cv2.EVENT_MBUTTONUP

RBUTTONDBLCLK = cv2.EVENT_RBUTTONDBLCLK
RBUTTONDOWN   = cv2.EVENT_RBUTTONDOWN
RBUTTONUP     = cv2.EVENT_RBUTTONUP

class Window:

    def onKey(self, keycode: int):
        """
        [virtual] Key press handler
        """
        pass

    def onWheel(self, pos, delta, vertical=True):
        pass

    def onMouseMove(self, pos: tuple[int, int], btn, flag):
        """
        [virtual] Mouse handler
        """
        pass

    last_mouse_down_pos = None
    last_mouse_down_btn = None

    def onMouseDown(self, pos: tuple[int, int], btn, flag):
        """
        [virtual] Mouse down handler
        """
        self.last_mouse_down_pos = pos
        self.last_mouse_down_btn = btn

    def onMouseUp(self, pos: tuple[int, int], btn, flag):
        """
        [virtual] Mouse up handler
        """
        if self.last_mouse_down_pos is not None:
            pos_src = self.last_mouse_down_pos
            pos_dst = pos
            btn_src = self.last_mouse_down_btn
            btn_dst = btn
            if btn_src == btn_dst:
                self.onMouseClick(
                    src=pos_src,
                    dst=pos_dst,
                    btn=btn
                )
            # Remove record
            self.last_mouse_down_pos = None
            self.last_mouse_down_btn = None

    def onMouseClick(self, src: tuple[int, int], dst: tuple[int, int], btn, flag):
        """
        [virtual] Mouse click handler
        Will be triggerred internally by other handlers
        """
        pass
        
    def __init__(self, name, flags=cv2.WINDOW_AUTOSIZE):
        self.name = name
        self.win_flags = flags

    def __enter__(self):
        # Generate click handler for this instance
        def mouse_handler(e, x, y, flag, param):
            pos = x, y
            btn = None
            if e in [LBUTTONDOWN, LBUTTONUP, LBUTTONDBLCLK]:
                btn = 0b100
            elif e in [MBUTTONDOWN, MBUTTONUP, MBUTTONDBLCLK]:
                btn = 0b010
            elif e in [RBUTTONDOWN, RBUTTONUP, RBUTTONDBLCLK]:
                btn = 0b001
            # Dispatch event
            if e in [LBUTTONDOWN, RBUTTONDOWN, MBUTTONDOWN]:
                self.onMouseDown(pos, btn, flag)
            elif e in [MOUSEMOVE]:
                self.onMouseMove(pos, btn, flag)
            elif e in [LBUTTONDOWN, RBUTTONDOWN, MBUTTONDOWN]:
                self.onMouseDown(pos, btn, flag)
            elif e in [MOUSEWHEEL, MOUSEWHEEL]:
                # self.onWheel(pos, param)
                print("Wheel event ignored", flag, param)
                pass
        # Declare window instance
        cv2.namedWindow(self.name)
        # Register callback
        cv2.setMouseCallback(self.name, mouse_handler)


    def __exit__(self, *exc_details):
        cv2.destroyWindow(self.name)

    def render(self, img: NDArray):
        cv2.imshow(self.name, types.U8(img))
