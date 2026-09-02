import ctypes
import platform
from pathlib import Path

class Error(Exception):
    pass

class Request(ctypes.Structure):
    _fields_ = [
        ("text", ctypes.c_char_p),
        ("instruction", ctypes.c_char_p),
        ("ref_text", ctypes.c_char_p),
        ("ref_audio", ctypes.POINTER(ctypes.c_float)),
        ("ref_audio_len", ctypes.c_int),
        ("cfg_scale", ctypes.c_float),
        ("seed", ctypes.c_int),
        ("max_new_tokens", ctypes.c_int),
        ("split_chars", ctypes.c_int),
        ("temperature", ctypes.c_float),
        ("top_k", ctypes.c_int),
        ("top_p", ctypes.c_float),
        ("repetition_penalty", ctypes.c_float),
    ]

Callback = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_int,
    ctypes.c_void_p,
)

def find_library(path=None):
    if path and Path(path).is_file():
        return Path(path).resolve()
    directory = Path(__file__).resolve().parent / "lib"
    system = platform.system()
    lookup = {
        "Darwin": "libbreeze.dylib",
        "Linux": "libbreeze.so",
        "Windows": "breeze.dll",
    }
    name = lookup.get(system, "libbreeze.so")
    library_file = directory / name
    if library_file.is_file():
        return library_file
    raise Error(f"Native library '{name}' not found in {directory}")

class Native:

    def __init__(self, path=None):
        self.path = find_library(path)
        try:
            self.library = ctypes.CDLL(str(self.path))
        except Exception as error:
            raise Error(f"Failed to load {self.path}: {error}") from error
        lib = self.library
        lib.breeze_init.restype = ctypes.c_void_p
        lib.breeze_init.argtypes = [ctypes.c_char_p, ctypes.c_int]
        lib.breeze_free.restype = None
        lib.breeze_free.argtypes = [ctypes.c_void_p]
        lib.breeze_sample_rate.restype = ctypes.c_int
        lib.breeze_sample_rate.argtypes = [ctypes.c_void_p]
        lib.breeze_generate.restype = ctypes.c_int
        lib.breeze_generate.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(Request),
            Callback,
            ctypes.c_void_p,
        ]
        lib.breeze_last_error.restype = ctypes.c_char_p
        lib.breeze_last_error.argtypes = []

    def get_error(self):
        message = self.library.breeze_last_error()
        return message.decode("utf-8", errors="replace") if message else "Unknown error"