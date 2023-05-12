# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
# Root class for objects that supports mouse and
# keyboard interactions
# --------------------------------------------------
import cv2
from ._key_code_ import KEYCODE
# from cv2 import \
#     FLAG_ALTKEY         as ALTKEY,        \
#     FLAG_CTRLKEY        as CTRLKEY,       \
#     FLAG_SHIFTKEY       as SHIFTKEY,      \
#     \
#     FLAG_LBUTTON        as LBUTTON,       \
#     FLAG_MBUTTON        as MBUTTON,       \
#     FLAG_RBUTTON        as RBUTTON,       \
#     \
#     EVENT_MOUSEMOVE     as MOUSEMOVE,     \
#     EVENT_MOUSEHWHEEL   as MOUSEHWHEEL,   \
#     EVENT_MOUSEWHEEL    as MOUSEWHEEL,    \
#     \
#     EVENT_LBUTTONDBLCLK as LBUTTONDBLCLK, \
#     EVENT_LBUTTONDOWN   as LBUTTONDOWN,   \
#     EVENT_LBUTTONUP     as LBUTTONUP,     \
#     \
#     EVENT_MBUTTONDBLCLK as MBUTTONDBLCLK, \
#     EVENT_MBUTTONDOWN   as MBUTTONDOWN,   \
#     EVENT_MBUTTONUP     as MBUTTONUP,     \
#     \
#     EVENT_RBUTTONDBLCLK as RBUTTONDBLCLK, \
#     EVENT_RBUTTONDOWN   as RBUTTONDOWN,   \
#     EVENT_RBUTTONUP     as RBUTTONUP      \
# --------------------------------------------------
class KeyboardInteractive:

    def onKey(self, keycode: int):
        """
        [virtual] Key press handler
        Falsy return value breaks main UI loop
        """
        return keycode != KEYCODE["escape"]
    
    def main_loop(self, waitKeyDuration: int = 16):
        while True:
            keycode = cv2.waitKey(waitKeyDuration)
            if keycode < 0:
                continue
            if not self.onKey(keycode):
                break

class MouseInteractive:

    def onMouse(self, evt, x: int, y: int, flags, param):
        """
        [virtual] Mouse event handler
        Falsy return value breaks main UI loop
        """
        return True

    def __handle_mouse__(self, window_name: str):
        # Register callback
        cv2.setMouseCallback(window_name, self.onMouse)
