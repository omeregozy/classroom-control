from Server import Server
from multiprocessing import Process, Pipe
import win32gui
from io import BytesIO
from PIL import ImageGrab, Image

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

    def student_start_stream(self, client):
        if self.streaming is not None:
            self.streaming.send("close stream".encode())
        else:
            super().send_tcp_to_all("start listening",client)
        self.streaming = client
        client.send("start streaming")

    def blackout_all(self):
        self.send_tcp_to_all(b"black out".zfill(20))

    def release_all(self):
        self.send_tcp_to_all(b"release black out".zfill(20))

    def blackout(self, client):
        client.send(b"black out".zfill(20))

    def release(self,  client):
        client.send(b"release black out".zfill(20))

    def broadcast_screen(self):
        pass