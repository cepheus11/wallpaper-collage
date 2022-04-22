from ctypes import CDLL, create_string_buffer, byref, c_int, c_void_p, c_char_p
from ctypes.util import find_library
import threading

# https://blog.abhi.host/blog/2010/10/18/changing-process-name-of-python-script/

_libc = None  # libc object from LibraryLoader: Instance of class CDLL
_libpthread = None


def pr_set_name(name: str):
    global _libc
    global _libpthread
    if _libc is None:
        _libc = CDLL(find_library('c'))
    assert(_libc is not None)
    if _libpthread is None:
        _libpthread = CDLL(find_library('pthread'))
    assert(_libpthread is not None)
#    thread_id = threading.current_thread().native_id
    n = name[:15]  # process names in linux are limited to 16 characters including null terminator
    buffer = create_string_buffer(n.encode("ascii"))  # space for null terminator?

    setname_func = _libc.prctl
    setname_func.argtypes = [c_int, c_void_p, c_int, c_int, c_int]
    setname_func.restype = c_int
    setname_func(15, byref(buffer), 0, 0, 0)  # from /usr/include/linux/prctl.h: #define PR_SET_NAME 15

    setname_func_2 = _libpthread.pthread_setname_np
    setname_func_2.argtypes = [c_int, c_char_p]
    setname_func_2.restype = c_int
#    setname_func_2(thread_id, b"wallpaper")
