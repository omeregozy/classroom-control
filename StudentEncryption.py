from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import time
class StudentEncryption:
    def __init__(self):
        self.key = get_random_bytes(32)
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt_key(self, public_key):
        public_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(self.key)

    def encrypt_message(self, data):
        return self.cipher.encrypt(pad(data,AES.block_size))

    def decrypt_message(self, data):
        return unpad(self.cipher.decrypt(data),AES.block_size)

files = [get_random_bytes(64000) for i in range(10000)]
enc = StudentEncryption()
encrypted_files = []
t = time.time()
for i in files:
    encrypted_files.append(enc.encrypt_message(i))
print(time.time()-t)
t = time.time()
for i in encrypted_files:
    enc.decrypt_message(i)
print(time.time()-t)