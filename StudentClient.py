from Client import Client
import re
import win32api
import win32con
import time
import math


class StudentClient(Client):
    def __init__(self, student_server, window):
        super().__init__(student_server.teacher_ip)
        super().open_tcp_connection()
        self.student_server = student_server
        self.window = window

    def listen_to_teacher(self, data):
        data = data.decode().lstrip('0')
        if data == "stream":
            self.student_server.stream_func = self.student_server.send_multicast
        elif data == "release stream":
            self.student_server.stream_func = self.student_server.send_to_teacher
        elif data == "start listening":
            self.window.display_screen()
        elif data == "stop listening":
            self.window.hide_screen()
        elif re.search("[0-9]*,[0-9]*", data[1:-1]):
            data = data[1:-1].split(',')
            win32api.SetCursorPos((int(data[0],int(data[1]))))
        elif data.startswith("press"):
            if data[-1] == 1:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            elif data[-1] == 3:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        elif data.startswith("release press"):
            if data[-1] == 1:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            elif data[-1] == 3:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)