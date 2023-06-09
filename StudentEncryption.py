from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class StudentEncryption:
    def __init__(self):
        self.key = get_random_bytes(32)
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt_key(self, public_key):
        public_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(self.key)

    def encrypt_message(self, data):
        if len(data)%16 != 0:
            data = pad(data,AES.block_size)
        return self.cipher.encrypt(data)

    def decrypt_message(self, data):
        try:
            return unpad(self.cipher.decrypt(data),AES.block_size)
        except:
            return self.cipher.decrypt(data)