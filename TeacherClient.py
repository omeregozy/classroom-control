from Client import Client
from io import BytesIO
from PIL import Image
import time

class TeacherClient(Client):
    def __init__(self):
        super().__init__()

    def get_img(self, data, addr, handle_img):
        len = int(data[:10].decode())
        img = data[10:len + 10]
        handle_img(addr, Image.open(BytesIO(img)))