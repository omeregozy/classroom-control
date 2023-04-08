import threading
from PIL import ImageGrab, Image
from Server import Server
import time
import PyWin32

import win32gui
from io import BytesIO

def get_screenshot():
    bio = BytesIO()
    quality = 5
    cursor = Image.open("cursor.png")
    print(cursor.mode == "RGBA")
    while True:
        img = ImageGrab.grab()
        img = img.convert("RGBA")
        img.alpha_composite(cursor, dest=win32gui.GetCursorPos())
        img = img.convert("RGB")
        img.thumbnail((1024,576))
        img.save(bio, "JPEG", quality=quality)
        bio.seek(0)
        img = bio.getvalue()
        bio.truncate(0)
        length = len(img)
        if length < 65400:
            return self.teacher_ip, str(len(img)).zfill(10).encode() + img[::-1].zfill(65400)[::-1])
            if quality < 95 and length < 55000:
                quality += 5
        else:
            quality -= 5

class StudentServer(Server):
    def __init__(self, teacher_ip):
        super().__init__()
        super().open_udp()
        super().open_multicast()
        self.teacher_ip = teacher_ip
        threading.Thread(target=self.send_image,args=[super().send_udp]).start()


