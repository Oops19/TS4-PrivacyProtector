# The most useful windows datatypes
import pp_ctypes

BYTE = pp_ctypes.c_byte
WORD = pp_ctypes.c_ushort
DWORD = pp_ctypes.c_ulong

#UCHAR = pp_ctypes.c_uchar
CHAR = pp_ctypes.c_char
WCHAR = pp_ctypes.c_wchar
UINT = pp_ctypes.c_uint
INT = pp_ctypes.c_int

DOUBLE = pp_ctypes.c_double
FLOAT = pp_ctypes.c_float

BOOLEAN = BYTE
BOOL = pp_ctypes.c_long

class VARIANT_BOOL(pp_ctypes._SimpleCData):
    _type_ = "v"
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)

ULONG = pp_ctypes.c_ulong
LONG = pp_ctypes.c_long

USHORT = pp_ctypes.c_ushort
SHORT = pp_ctypes.c_short

# in the windows header files, these are structures.
_LARGE_INTEGER = LARGE_INTEGER = pp_ctypes.c_longlong
_ULARGE_INTEGER = ULARGE_INTEGER = pp_ctypes.c_ulonglong

LPCOLESTR = LPOLESTR = OLESTR = pp_ctypes.c_wchar_p
LPCWSTR = LPWSTR = pp_ctypes.c_wchar_p
LPCSTR = LPSTR = pp_ctypes.c_char_p
LPCVOID = LPVOID = pp_ctypes.c_void_p

# WPARAM is defined as UINT_PTR (unsigned type)
# LPARAM is defined as LONG_PTR (signed type)
if pp_ctypes.sizeof(pp_ctypes.c_long) == pp_ctypes.sizeof(pp_ctypes.c_void_p):
    WPARAM = pp_ctypes.c_ulong
    LPARAM = pp_ctypes.c_long
elif pp_ctypes.sizeof(pp_ctypes.c_longlong) == pp_ctypes.sizeof(pp_ctypes.c_void_p):
    WPARAM = pp_ctypes.c_ulonglong
    LPARAM = pp_ctypes.c_longlong

ATOM = WORD
LANGID = WORD

COLORREF = DWORD
LGRPID = DWORD
LCTYPE = DWORD

LCID = DWORD

################################################################
# HANDLE types
HANDLE = pp_ctypes.c_void_p # in the header files: void *

HACCEL = HANDLE
HBITMAP = HANDLE
HBRUSH = HANDLE
HCOLORSPACE = HANDLE
HDC = HANDLE
HDESK = HANDLE
HDWP = HANDLE
HENHMETAFILE = HANDLE
HFONT = HANDLE
HGDIOBJ = HANDLE
HGLOBAL = HANDLE
HHOOK = HANDLE
HICON = HANDLE
HINSTANCE = HANDLE
HKEY = HANDLE
HKL = HANDLE
HLOCAL = HANDLE
HMENU = HANDLE
HMETAFILE = HANDLE
HMODULE = HANDLE
HMONITOR = HANDLE
HPALETTE = HANDLE
HPEN = HANDLE
HRGN = HANDLE
HRSRC = HANDLE
HSTR = HANDLE
HTASK = HANDLE
HWINSTA = HANDLE
HWND = HANDLE
SC_HANDLE = HANDLE
SERVICE_STATUS_HANDLE = HANDLE

################################################################
# Some important structure definitions

class RECT(pp_ctypes.Structure):
    _fields_ = [("left", LONG),
                ("top", LONG),
                ("right", LONG),
                ("bottom", LONG)]
tagRECT = _RECTL = RECTL = RECT

class _SMALL_RECT(pp_ctypes.Structure):
    _fields_ = [('Left', SHORT),
                ('Top', SHORT),
                ('Right', SHORT),
                ('Bottom', SHORT)]
SMALL_RECT = _SMALL_RECT

class _COORD(pp_ctypes.Structure):
    _fields_ = [('X', SHORT),
                ('Y', SHORT)]

class POINT(pp_ctypes.Structure):
    _fields_ = [("x", LONG),
                ("y", LONG)]
tagPOINT = _POINTL = POINTL = POINT

class SIZE(pp_ctypes.Structure):
    _fields_ = [("cx", LONG),
                ("cy", LONG)]
tagSIZE = SIZEL = SIZE

def RGB(red, green, blue):
    return red + (green << 8) + (blue << 16)

class FILETIME(pp_ctypes.Structure):
    _fields_ = [("dwLowDateTime", DWORD),
                ("dwHighDateTime", DWORD)]
_FILETIME = FILETIME

class MSG(pp_ctypes.Structure):
    _fields_ = [("hWnd", HWND),
                ("message", UINT),
                ("wParam", WPARAM),
                ("lParam", LPARAM),
                ("time", DWORD),
                ("pt", POINT)]
tagMSG = MSG
MAX_PATH = 260

class WIN32_FIND_DATAA(pp_ctypes.Structure):
    _fields_ = [("dwFileAttributes", DWORD),
                ("ftCreationTime", FILETIME),
                ("ftLastAccessTime", FILETIME),
                ("ftLastWriteTime", FILETIME),
                ("nFileSizeHigh", DWORD),
                ("nFileSizeLow", DWORD),
                ("dwReserved0", DWORD),
                ("dwReserved1", DWORD),
                ("cFileName", CHAR * MAX_PATH),
                ("cAlternateFileName", CHAR * 14)]

class WIN32_FIND_DATAW(pp_ctypes.Structure):
    _fields_ = [("dwFileAttributes", DWORD),
                ("ftCreationTime", FILETIME),
                ("ftLastAccessTime", FILETIME),
                ("ftLastWriteTime", FILETIME),
                ("nFileSizeHigh", DWORD),
                ("nFileSizeLow", DWORD),
                ("dwReserved0", DWORD),
                ("dwReserved1", DWORD),
                ("cFileName", WCHAR * MAX_PATH),
                ("cAlternateFileName", WCHAR * 14)]

################################################################
# Pointer types

LPBOOL = PBOOL = pp_ctypes.POINTER(BOOL)
PBOOLEAN = pp_ctypes.POINTER(BOOLEAN)
LPBYTE = PBYTE = pp_ctypes.POINTER(BYTE)
PCHAR = pp_ctypes.POINTER(CHAR)
LPCOLORREF = pp_ctypes.POINTER(COLORREF)
LPDWORD = PDWORD = pp_ctypes.POINTER(DWORD)
LPFILETIME = PFILETIME = pp_ctypes.POINTER(FILETIME)
PFLOAT = pp_ctypes.POINTER(FLOAT)
LPHANDLE = PHANDLE = pp_ctypes.POINTER(HANDLE)
PHKEY = pp_ctypes.POINTER(HKEY)
LPHKL = pp_ctypes.POINTER(HKL)
LPINT = PINT = pp_ctypes.POINTER(INT)
PLARGE_INTEGER = pp_ctypes.POINTER(LARGE_INTEGER)
PLCID = pp_ctypes.POINTER(LCID)
LPLONG = PLONG = pp_ctypes.POINTER(LONG)
LPMSG = PMSG = pp_ctypes.POINTER(MSG)
LPPOINT = PPOINT = pp_ctypes.POINTER(POINT)
PPOINTL = pp_ctypes.POINTER(POINTL)
LPRECT = PRECT = pp_ctypes.POINTER(RECT)
LPRECTL = PRECTL = pp_ctypes.POINTER(RECTL)
LPSC_HANDLE = pp_ctypes.POINTER(SC_HANDLE)
PSHORT = pp_ctypes.POINTER(SHORT)
LPSIZE = PSIZE = pp_ctypes.POINTER(SIZE)
LPSIZEL = PSIZEL = pp_ctypes.POINTER(SIZEL)
PSMALL_RECT = pp_ctypes.POINTER(SMALL_RECT)
LPUINT = PUINT = pp_ctypes.POINTER(UINT)
PULARGE_INTEGER = pp_ctypes.POINTER(ULARGE_INTEGER)
PULONG = pp_ctypes.POINTER(ULONG)
PUSHORT = pp_ctypes.POINTER(USHORT)
PWCHAR = pp_ctypes.POINTER(WCHAR)
LPWIN32_FIND_DATAA = PWIN32_FIND_DATAA = pp_ctypes.POINTER(WIN32_FIND_DATAA)
LPWIN32_FIND_DATAW = PWIN32_FIND_DATAW = pp_ctypes.POINTER(WIN32_FIND_DATAW)
LPWORD = PWORD = pp_ctypes.POINTER(WORD)
