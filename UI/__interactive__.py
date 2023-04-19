# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
# Root class for objects that supports mouse and
# keyboard interactions
# --------------------------------------------------
import cv2
# FLAG_ALTKEY, \
# FLAG_CTRLKEY, \
# FLAG_SHIFTKEY, \
# \
# FLAG_LBUTTON, \
# FLAG_MBUTTON, \
# FLAG_RBUTTON, \
# \
from cv2 import \
    EVENT_MOUSEMOVE as MOUSEMOVE, \
    EVENT_MOUSEHWHEEL as MOUSEHWHEEL, \
    EVENT_MOUSEWHEEL as MOUSEWHEEL, \
    \
    EVENT_LBUTTONDBLCLK as LBUTTONDBLCLK, \
    EVENT_LBUTTONDOWN as LBUTTONDOWN, \
    EVENT_LBUTTONUP as LBUTTONUP, \
    \
    EVENT_MBUTTONDBLCLK as MBUTTONDBLCLK, \
    EVENT_MBUTTONDOWN as MBUTTONDOWN, \
    EVENT_MBUTTONUP as MBUTTONUP, \
    \
    EVENT_RBUTTONDBLCLK as RBUTTONDBLCLK, \
    EVENT_RBUTTONDOWN as RBUTTONDOWN, \
    EVENT_RBUTTONUP as RBUTTONUP \
# --------------------------------------------------
class Interactive:

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

    __down_pos__ = None
    __down_btn__ = None

    def onMouseDown(self, pos: tuple[int, int], btn, flag):
        """
        [virtual] Mouse down handler
        """
        self.__down_pos__ = pos
        self.__down_btn__ = btn

    def onMouseUp(self, pos: tuple[int, int], btn, flag):
        """
        [virtual] Mouse up handler
        """
        if self.__down_pos__ is not None:
            pos_src = self.__down_pos__
            pos_dst = pos
            btn_src = self.__down_btn__
            btn_dst = btn
            if btn_src == btn_dst:
                self.onMouseClick(
                    src=pos_src,
                    dst=pos_dst,
                    btn=btn
                )
            # Remove record
            self.__down_pos__ = None
            self.__down_btn__ = None

    def onMouseClick(self, src: tuple[int, int], dst: tuple[int, int], btn, flag):
        """
        [virtual] Mouse click handler
        Will be triggered internally by other handlers
        """
        pass

    def registerMouseCallback(self, window_name: str):
        # Generate click handler for this instance
        def handler(e, x, y, flag, param):
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
        # Register callback
        cv2.setMouseCallback(window_name, handler)

