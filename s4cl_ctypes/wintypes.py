# The most useful windows datatypes
import s4cl_ctypes

BYTE = s4cl_ctypes.c_byte
WORD = s4cl_ctypes.c_ushort
DWORD = s4cl_ctypes.c_ulong

#UCHAR = s4cl_ctypes.c_uchar
CHAR = s4cl_ctypes.c_char
WCHAR = s4cl_ctypes.c_wchar
UINT = s4cl_ctypes.c_uint
INT = s4cl_ctypes.c_int

DOUBLE = s4cl_ctypes.c_double
FLOAT = s4cl_ctypes.c_float

BOOLEAN = BYTE
BOOL = s4cl_ctypes.c_long

class VARIANT_BOOL(s4cl_ctypes._SimpleCData):
    _type_ = "v"
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)

ULONG = s4cl_ctypes.c_ulong
LONG = s4cl_ctypes.c_long

USHORT = s4cl_ctypes.c_ushort
SHORT = s4cl_ctypes.c_short

# in the windows header files, these are structures.
_LARGE_INTEGER = LARGE_INTEGER = s4cl_ctypes.c_longlong
_ULARGE_INTEGER = ULARGE_INTEGER = s4cl_ctypes.c_ulonglong

LPCOLESTR = LPOLESTR = OLESTR = s4cl_ctypes.c_wchar_p
LPCWSTR = LPWSTR = s4cl_ctypes.c_wchar_p
LPCSTR = LPSTR = s4cl_ctypes.c_char_p
LPCVOID = LPVOID = s4cl_ctypes.c_void_p

# WPARAM is defined as UINT_PTR (unsigned type)
# LPARAM is defined as LONG_PTR (signed type)
if s4cl_ctypes.sizeof(s4cl_ctypes.c_long) == s4cl_ctypes.sizeof(s4cl_ctypes.c_void_p):
    WPARAM = s4cl_ctypes.c_ulong
    LPARAM = s4cl_ctypes.c_long
elif s4cl_ctypes.sizeof(s4cl_ctypes.c_longlong) == s4cl_ctypes.sizeof(s4cl_ctypes.c_void_p):
    WPARAM = s4cl_ctypes.c_ulonglong
    LPARAM = s4cl_ctypes.c_longlong

ATOM = WORD
LANGID = WORD

COLORREF = DWORD
LGRPID = DWORD
LCTYPE = DWORD

LCID = DWORD

################################################################
# HANDLE types
HANDLE = s4cl_ctypes.c_void_p # in the header files: void *

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

class RECT(s4cl_ctypes.Structure):
    _fields_ = [("left", LONG),
                ("top", LONG),
                ("right", LONG),
                ("bottom", LONG)]
tagRECT = _RECTL = RECTL = RECT

class _SMALL_RECT(s4cl_ctypes.Structure):
    _fields_ = [('Left', SHORT),
                ('Top', SHORT),
                ('Right', SHORT),
                ('Bottom', SHORT)]
SMALL_RECT = _SMALL_RECT

class _COORD(s4cl_ctypes.Structure):
    _fields_ = [('X', SHORT),
                ('Y', SHORT)]

class POINT(s4cl_ctypes.Structure):
    _fields_ = [("x", LONG),
                ("y", LONG)]
tagPOINT = _POINTL = POINTL = POINT

class SIZE(s4cl_ctypes.Structure):
    _fields_ = [("cx", LONG),
                ("cy", LONG)]
tagSIZE = SIZEL = SIZE

def RGB(red, green, blue):
    return red + (green << 8) + (blue << 16)

class FILETIME(s4cl_ctypes.Structure):
    _fields_ = [("dwLowDateTime", DWORD),
                ("dwHighDateTime", DWORD)]
_FILETIME = FILETIME

class MSG(s4cl_ctypes.Structure):
    _fields_ = [("hWnd", HWND),
                ("message", UINT),
                ("wParam", WPARAM),
                ("lParam", LPARAM),
                ("time", DWORD),
                ("pt", POINT)]
tagMSG = MSG
MAX_PATH = 260

class WIN32_FIND_DATAA(s4cl_ctypes.Structure):
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

class WIN32_FIND_DATAW(s4cl_ctypes.Structure):
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

LPBOOL = PBOOL = s4cl_ctypes.POINTER(BOOL)
PBOOLEAN = s4cl_ctypes.POINTER(BOOLEAN)
LPBYTE = PBYTE = s4cl_ctypes.POINTER(BYTE)
PCHAR = s4cl_ctypes.POINTER(CHAR)
LPCOLORREF = s4cl_ctypes.POINTER(COLORREF)
LPDWORD = PDWORD = s4cl_ctypes.POINTER(DWORD)
LPFILETIME = PFILETIME = s4cl_ctypes.POINTER(FILETIME)
PFLOAT = s4cl_ctypes.POINTER(FLOAT)
LPHANDLE = PHANDLE = s4cl_ctypes.POINTER(HANDLE)
PHKEY = s4cl_ctypes.POINTER(HKEY)
LPHKL = s4cl_ctypes.POINTER(HKL)
LPINT = PINT = s4cl_ctypes.POINTER(INT)
PLARGE_INTEGER = s4cl_ctypes.POINTER(LARGE_INTEGER)
PLCID = s4cl_ctypes.POINTER(LCID)
LPLONG = PLONG = s4cl_ctypes.POINTER(LONG)
LPMSG = PMSG = s4cl_ctypes.POINTER(MSG)
LPPOINT = PPOINT = s4cl_ctypes.POINTER(POINT)
PPOINTL = s4cl_ctypes.POINTER(POINTL)
LPRECT = PRECT = s4cl_ctypes.POINTER(RECT)
LPRECTL = PRECTL = s4cl_ctypes.POINTER(RECTL)
LPSC_HANDLE = s4cl_ctypes.POINTER(SC_HANDLE)
PSHORT = s4cl_ctypes.POINTER(SHORT)
LPSIZE = PSIZE = s4cl_ctypes.POINTER(SIZE)
LPSIZEL = PSIZEL = s4cl_ctypes.POINTER(SIZEL)
PSMALL_RECT = s4cl_ctypes.POINTER(SMALL_RECT)
LPUINT = PUINT = s4cl_ctypes.POINTER(UINT)
PULARGE_INTEGER = s4cl_ctypes.POINTER(ULARGE_INTEGER)
PULONG = s4cl_ctypes.POINTER(ULONG)
PUSHORT = s4cl_ctypes.POINTER(USHORT)
PWCHAR = s4cl_ctypes.POINTER(WCHAR)
LPWIN32_FIND_DATAA = PWIN32_FIND_DATAA = s4cl_ctypes.POINTER(WIN32_FIND_DATAA)
LPWIN32_FIND_DATAW = PWIN32_FIND_DATAW = s4cl_ctypes.POINTER(WIN32_FIND_DATAW)
LPWORD = PWORD = s4cl_ctypes.POINTER(WORD)
