import pywintypes

from Window import Window
import threading
import win32gui
import win32con
import win32api
import time

class StudentGui(Window):
    def __init__(self,server):
        super().__init__()
        self.server = server
        self.create_text_label("Welcome student")
        self.create_button_label(None, text="send message to teacher")
        self.create_button_label(None, text="request to stream your screen")

class FullScreenWindow(Window):
    def __init__(self):
        super().__init__(resizable=False,title="full screen student program")
        def disable_close():
            pass
        self.root.protocol("WM_DELETE_WINDOW", disable_close)
        self.root.attributes("-fullscreen", True)
        self.window_exist = True
        self.start_function(self.close, 20000)
        self.start_function(self.remain_in_the_front,5)

    def remain_in_the_front(self):
        def check_if_in_the_front():
            HWND = win32gui.FindWindow(None, "full screen student program")
            while self.window_exist:
                if win32gui.GetForegroundWindow() != HWND:
                    print("front")
                    win32gui.ShowWindow(HWND, win32con.SW_RESTORE)
                    win32gui.SetWindowPos(HWND, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                          win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                    win32gui.SetActiveWindow(HWND)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    time.sleep(0.01)
        threading.Thread(target=check_if_in_the_front).start()

    def close(self):
        self.window_exist = False
        time.sleep(0.5)
        self.start_function(self.destroy, 0)

window = FullScreenWindow()
window.start()