from Client import Client
from io import BytesIO
from PIL import Image

class TeacherClient(Client):
    def __init__(self,encryption):
        super().__init__()
        self.encryption = encryption

    def get_img(self, data, addr, handle_img, decrypt):
        if decrypt:
            data = self.encryption.decrypt(data, addr)
        len = int(data[:10].decode())
        img = data[10:len + 10]
        try:
            handle_img(addr, Image.open(BytesIO(img)))
        except:
            pass