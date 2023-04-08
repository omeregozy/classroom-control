from Client import Client
from io import BytesIO
from PIL import Image
import time

class TeacherClient(Client):
    def __init__(self):
        super().__init__()

    def get_img(self, data, func, *args):
        len = int(data[:10].decode())
        img = data[10:len + 10]
        return Image.open(BytesIO(img))