# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import types, misc
# --------------------------------------------------


def D3(img: NDArray) -> NDArray:
    """
    Add 3rd dimension to an array if it's not.
    Use <NDArray>.squeeze() to revert this operation.
    """
    shape = list(img.shape)
    ndim = img.ndim
    assert ndim == len(shape), f"len({shape}) != {ndim}"
    if ndim == 2:
        # Expand to 3D array, with 3rd dimension only have 1 layer
        return img.reshape(shape + [-1])
    else:
        assert ndim == 3, f"{ndim} != 3"
        return img


def text(pos=None, font=cv2.FONT_HERSHEY_PLAIN, scale=0.5, color=[255] * 3, width=1):
    color = list(map(int, color))

    def apply(img: NDArray, txt: str):
        nonlocal pos, font, scale, color, width
        if pos is None:
            pos = (10, img.shape[0] - 10)
        img = types.U8(img)
        return cv2.putText(
            img, txt, pos, font,
            scale, color, width,
            cv2.LINE_AA
        )
    return apply


def pad(*sizes: int, color: NDArray[np.floating] | float | int = 0, top=None, left=None, bottom=None, right=None):
    """
    (Lambda) Pad the given image by given widths on each size.
        The size parameter can be a scalar or an array of 1/2/4 elements.
    0 element : no padding
    1 element : all sides
    2 elements: [vertical, horizontal]
    4 elements: [top, right, bottom, left]
    """
    args = list(map(int, sizes))
    match len(args):
        case 0: args = [0] * 4
        case 1: args = args * 4
        case 2: args = args * 2
        case n:
            assert n == 4, f"Unable to use {n} arugments for padding size"
    if top is None:
        top = args[0]
    if left is None:
        left = args[1]
    if bottom is None:
        bottom = args[2]
    if right is None:
        right = args[3]

    def apply(img: NDArray):
        nonlocal top, right, bottom, left, color
        img = misc.D3(img)
        h, w, d = img.shape
        # Caculate color if applicable (black)
        if isinstance(color, np.ndarray):
            tmp = np.zeros((d,), dtype=color.dtype)
        elif isinstance(color, int):
            tmp = np.zeros((d,), dtype=np.uint8)
        elif isinstance(color, float):
            tmp = np.zeros((d,), dtype=np.float32)
        else:
            assert False, f"Unknown type for color: {type(color)}"
        tmp[:] = color
        # Match type of color with type of image
        color = types.MatchType(img)(tmp).reshape((1, 1, -1))
        # Create an empty canvas with padding color
        canvas = np.zeros(
            (left + right + h, top + bottom + w, d), dtype=img.dtype)
        # Broadcast padding color into canvas
        canvas[:, :] = color
        # Put image into its position
        canvas[bottom:bottom+h, left:left+w] = img
        # Return in original dimensions
        return canvas.squeeze()
    return apply
