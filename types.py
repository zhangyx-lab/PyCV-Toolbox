# --------------------------------------------------
# PyCV-Toolbox by Yuxuan Zhang (zhangyuxuan@ufl.edu)
# --------------------------------------------------
from .__internal__ import *
from . import fx, histogram
# --------------------------------------------------


def trimToFit(img: NDArray, lim=[0, 1]) -> NDArray:
    # Trim left side
    img[img < lim[0]] = lim[0]
    # Trim right side
    img[img > lim[1]] = lim[1]
    return img


def scaleToFit(img: NDArray, lim=[0, 1]) -> NDArray:
    # Caculate source dynamic range
    drange = [np.min(img), np.max(img)]
    # Check if image is uniform
    if drange[0] == drange[1]:
        img += 0.5 - np.average(drange)
        return img
    # Create numerical projection
    projection = fx.project(drange, lim)
    # Apply to image and return
    return projection(img)


def scaleToFitDR(img: NDArray, pos=[0.05, 0.95], dr=None, lim=[0, 1]) -> NDArray:
    """Scale the values inside a image to fit dynamic range"""
    if dr is None:
        dr = pos
    # Caculate source dynamic range
    dynamic = histogram.dynamic(*pos)
    drange = dynamic(img)
    # Check if image is uniform
    if drange[0] == drange[1]:
        img = np.average(drange)
        return img
    # Create numerical projection
    projection = fx.project(drange, dr)
    # Apply to image and return
    return trimToFit(projection(img), lim)


def _check_overflow(img: np.floating, lim=[0, 1], handler=None):
    if handler is None:
        assert np.min(img) >= lim[0], np.min(img)
        assert np.max(img) <= lim[1], np.max(img)
        return img
    else:
        return handler(img, lim)


def _bitwidth(dtype: np.dtype) -> int | None:
    match dtype:
        case np.uint8: return 8
        case np.uint16: return 16
        case np.uint32: return 32
        case np.uint64: return 64
        # case np.uint128: return 128
        # case np.uint256: return 256
        case np.float16: return 16
        case np.float32: return 32
        case np.float64: return 64
        # case np.float128: return 128
        # case np.float256: return 256
        case unknown: assert False, unknown


def _dtype_max(dtype: np.unsignedinteger) -> int:
    x = np.zeros((1,), dtype=dtype)
    return (~x)[0]


def to_unsigned(img: NDArray, dtype: np.unsignedinteger = None, fit=None) -> np.unsignedinteger:
    if not isinstance(img, np.ndarray):
        return np.array(img, dtype=np.uint32)
    if dtype is None:
        dtype = np.uint32
    src = _bitwidth(img.dtype)
    dst = _bitwidth(dtype)
    if issubclass(img.dtype.type, np.floating):
        img = _check_overflow(img, handler=fit)
        return (img * _dtype_max(dtype)).astype(dtype)
    elif src < dst:
        return img.astype(dtype) << (dst - src)
    elif src > dst:
        return (img >> (src - dst)).astype(dtype)
    else:
        assert src == dst, f"{src} digits != {dst} digits"
        return img.copy()


def to_float(img: NDArray, dtype: np.floating = None) -> np.floating:
    if not isinstance(img, np.ndarray):
        return np.array(img, dtype=np.float32)
    if issubclass(img.dtype.type, np.floating):
        if dtype is None or img.dtype == dtype:
            return img.copy()
        else:
            return img.astype(dtype)
    else:
        assert issubclass(img.dtype.type, np.unsignedinteger), img.dtype
        if dtype is None:
            dtype = np.float32
        return img.astype(dtype) / _dtype_max(img.dtype)


def U8(img: NDArray, fit=trimToFit) -> NDArray[np.uint8]:
    return to_unsigned(img, np.uint8, fit)


def U16(img: NDArray, fit=trimToFit) -> NDArray[np.uint16]:
    return to_unsigned(img, np.uint16, fit)


def U32(img: NDArray, fit=trimToFit) -> NDArray[np.uint32]:
    return to_unsigned(img, np.uint32, fit)


def U64(img: NDArray, fit=trimToFit) -> NDArray[np.uint64]:
    return to_unsigned(img, np.uint64, fit)


def F16(img: NDArray) -> NDArray[np.float16]:
    return to_float(img, np.float16)


def F32(img: NDArray) -> NDArray[np.float32]:
    return to_float(img, np.float32)


def F64(img: NDArray) -> NDArray[np.float64]:
    return to_float(img, np.float64)


# def F128(img: NDArray) -> NDArray[np.float128]:
    # return to_float(img, np.float128)


# def F256(img: NDArray) -> NDArray[np.float256]:
    # return to_float(img, np.float256)


def MatchType(target: NDArray | np.dtype, fit=trimToFit):
    # Normalize target
    if isinstance(target, np.ndarray):
        target = target.dtype.type
    elif isinstance(target, np.dtype):
        target = target.type
    # Check for destination
    if issubclass(target, np.floating):
        """float -> float | uint -> float"""
        return lambda img: to_float(img, target)
    else:
        """uint -> uint | float -> uint"""
        assert issubclass(target, np.unsignedinteger), target
        return lambda img: to_unsigned(img, target, fit)
