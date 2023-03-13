from Client import Client
from io import BytesIO
from PIL import Image
import time

class TeacherClient(Client):
    def __init__(self):
        super().__init__()

    def get_img(self, data, func, *args):
        img, addr = self.udp_client.recvfrom(int(data.decode()))
        img = Image.open(BytesIO(img))
        func(img, *args)