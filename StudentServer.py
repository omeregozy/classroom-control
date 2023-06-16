import threading
from PIL import ImageGrab, Image
from Server import Server
from multiprocessing import Process, Pipe
import win32gui
from io import BytesIO

size = (256, 144)
cursor = Image.open("cursor.png")


def change_size(conn):
    global size, cursor
    real_cursor = cursor
    real_cursor_size = cursor.size
    cursor = cursor.resize(tuple(int(i/(2048/size[0])) for i in real_cursor_size))
    while True:
        size = conn.recv()
        cursor = real_cursor.resize(tuple(int(i / (2048 / size[0])) for i in real_cursor_size))


def get_screenshots(conn):
    threading.Thread(target=change_size, args=[conn]).start()
    bio = BytesIO()
    quality = 95
    while True:
        img = ImageGrab.grab()
        img.thumbnail(size)
        img = img.convert("RGBA")
        cursor_pos = win32gui.GetCursorPos()
        img.alpha_composite(cursor, dest=(int(cursor_pos[0] / (2048 / size[0])), int(cursor_pos[1] / (2048 / size[0])) + (2 * cursor.size[1])))
        img = img.convert("RGB")
        length = 65409
        while length > 65408:
            img.save(bio, "JPEG", quality=quality)
            bio.seek(0)
            img_file = bio.getvalue()
            bio.truncate(0)
            length = len(img_file)
            if length < 653998:
                conn.send_bytes(str(len(img_file)).zfill(10).encode() + img_file[::-1].zfill(653998)[::-1])
                if quality < 100 and length < 55000:
                    quality += 5
            else:
                quality -= 5


class StudentServer(Server):
    def __init__(self, teacher_ip, encryption):
        super().__init__()
        super().open_udp()
        super().open_multicast()
        self.encryption = encryption
        self.teacher_ip = teacher_ip
        self.send_to_teacher = lambda msg: self.send_udp(teacher_ip,msg)
        self.stream_func = self.send_to_teacher
        self.conn = None

    def send_screenshots(self):
        self.conn, conn2 = Pipe(duplex=True)
        Process(target=get_screenshots, args=[conn2]).start()
        while True:
            if self.stream_func is self.send_to_teacher:
                self.stream_func(self.encryption.encrypt(self.conn.recv_bytes()))
            else:
                self.stream_func(self.conn.recv_bytes())

    def change_screenshot_size(self, screen_size):
        self.conn.send(screen_size)


