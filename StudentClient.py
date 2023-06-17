from Client import Client
import win32api
import win32con
from PIL import Image
from io import BytesIO
import socket
import struct


class StudentClient(Client):
    def __init__(self, queue, encryption):
        key, self.remote_ip = self.get_public_key()
        super().__init__(self.remote_ip)
        super().open_tcp_connection()
        self.encryption = encryption
        self.tcp_client.send(encryption.encrypt_key(key))
        self.queue = queue
        self.student_server = None

    def add_server(self,server):
        self.student_server = server

    def listen_to_teacher(self, data):
        data = self.encryption.decrypt(data).decode()
        if data == "stream":
            self.student_server.change_screenshot_size((2048, 1152))
            self.student_server.stream_func = self.student_server.send_multicast
        elif data == "release stream":
            self.student_server.change_screenshot_size((256, 144))
            self.student_server.stream_func = self.student_server.send_to_teacher
        elif data == "start listening":
             self.queue.put("stream")
        elif data == "stop listening":
            self.queue.put("close")
        elif data == "blackout":
            self.queue.put("blackout")
        elif data == "stop blackout":
            self.queue.put("close")
        elif data == "full screen":
            self.student_server.change_screenshot_size((1024,576))
        elif data == "normal screen":
            self.student_server.change_screenshot_size((256, 144))
        elif data[0] == '(' and data[-1] == ')':
            data = data[1:-1].split(',')
            win32api.SetCursorPos((int(data[0])*2, int(data[1])*2))
        elif data.startswith("press"):
            if data[-1] == "1":
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
            elif data[-1] == "3":
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0,0,0)
        elif data.startswith("release press"):
            if data[-1] == "1":
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0,0,0)
            elif data[-1] == "3":
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0,0,0)

    def get_img(self, data, addr, handle_img):
        data = self.encryption.decrypt(data)
        len = int(data[:10].decode())
        img = data[10:len + 10]
        try:
            handle_img(Image.open(BytesIO(img)))
        except:
            pass

    def get_public_key(self):
        multicast_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        multicast_client.bind(("", 100))
        group = socket.inet_aton(self.multicast_ip)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        multicast_client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        data, addr = multicast_client.recvfrom(128)
        multicast_client.close()
        return data, addr
