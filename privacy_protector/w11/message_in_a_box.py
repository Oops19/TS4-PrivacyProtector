import s4cl_ctypes


class MessageInABox:
    @staticmethod
    def show_message_box(hwnd, title: str, message: str, u_type=0x00000010):
        """
        MB_OK = 0x00000000
        MB_ICONINFORMATION = 0x00000040
        MB_TASKMODAL = 0x00002000
        MB_ICONSTOP = 0x00000010
        """
        MessageBoxA = s4cl_ctypes.windll.user32.MessageBoxA
        MessageBoxA(hwnd, message.encode('UTF-8'), title.encode('UTF-8'), u_type)
