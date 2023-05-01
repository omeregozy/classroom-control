from Server import Server
from multiprocessing import Process, Pipe
import win32gui
from io import BytesIO
from PIL import ImageGrab, Image
import threading

send = True
def stop(conn):
    conn.recv_bytes()
    global send
    send = False
def get_screenshots(conn):
    cursor = Image.open("cursor.png")
    threading.Thread(target=stop, args=[conn]).start()
    bio = BytesIO()
    quality = 95
    while send:
        img = ImageGrab.grab()
        img = img.convert("RGBA")
        cursor_pos = win32gui.GetCursorPos()
        img.alpha_composite(cursor, dest=(cursor_pos[0], cursor_pos[1]))
        img = img.convert("RGB")
        length = 65401
        while length > 65400:
            img.save(bio, "JPEG", quality=quality)
            bio.seek(0)
            img_file = bio.getvalue()
            bio.truncate(0)
            length = len(img_file)
            if length < 65400:
                conn.send_bytes(str(len(img_file)).zfill(10).encode() + img_file[::-1].zfill(65400)[::-1])
                if quality < 95 and length < 55000:
                    quality += 5
            else:
                quality -= 5

class TeacherServer(Server):
    def __init__(self):
        super().__init__()
        super().open_tcp()
        super().open_multicast()
        self.streaming = None
        self.conn = None

    def student_start_stream(self, client):
        if self.streaming is not None:
            if self.streaming is self:
                self.conn.send_bytes(b"close")
            else:
                self.streaming.send(b"close stream".zfill(20))
        else:
            super().send_tcp_to_all(b"start listening".zfill(20),client)
        self.streaming = client
        client.send(b"start streaming")

    def blackout_all(self):
        self.send_tcp_to_all(b"black out".zfill(20))

    def release_blackout_all(self):
        self.send_tcp_to_all(b"release black out".zfill(20))

    def blackout(self, client):
        client.send(b"black out".zfill(20))

    def release_blackout(self,  client):
        client.send(b"release black out".zfill(20))

    def control(self, client):
        client.send(b"control".zfill(20))

    def release_control(self, client):
        client.send(b"release control".zfill(20))

    def stream_student(self, client):
        client.send(b"stream".zfill(20))

    def release_stream_student(self, client):
        client.send(b"release stream".zfill(20))

    def stream_screen(self):
        def send_screenshots():
            while self.streaming is self:
                self.send_multicast(self.conn.recv_bytes())
            self.conn.send_bytes(b"close")
        self.streaming = self
        self.conn, conn = Pipe(duplex=True)
        Process(target=get_screenshots, args=[conn]).start()
        threading.Thread(target=send_screenshots).start()


