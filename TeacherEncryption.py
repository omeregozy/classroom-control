from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import socket
import time
from Server import MULTICAST_GROUP
import threading

MULTICAST_PORT = 100

class TeacherEncryption:
    def __init__(self):
        self.ip_to_AES_cipher = {}
        self.private_RSA_key = RSA.generate(2048)
        self.public_RSA_key = self.private_RSA_key.public_key().export_key()
        self.RSA_cipher = PKCS1_OAEP.new(self.private_RSA_key)
        threading.Thread(target=self.send_public_key).start()

    def add_student(self, addr, data):
        key = self.RSA_cipher.decrypt(data)
        self.ip_to_AES_cipher[addr] = AES.new(key, AES.MODE_ECB)

    def decrypt_message(self, data, addr):
        return unpad(self.ip_to_AES_cipher[addr].decrypt(data),AES.block_size)

    def encrypt_message(self, data, addr):
        return self.ip_to_AES_cipher[addr].encrypt(pad(data,AES.block_size))

    def send_public_key(self):
        multicast_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        multicast_server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
        while True:
            multicast_server.sendto(self.public_RSA_key, (MULTICAST_GROUP, MULTICAST_PORT))
            time.sleep(5)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 200))
sock.listen()
client, addr = sock.accept()
enc = TeacherEncryption()
client.send(enc.public_RSA_key)
addr = "127.0.0.1"
enc.add_student(addr, client.recv(2024))
client.send(enc.encrypt_message(b"msg", "127.0.0.1"))
print(enc.decrypt_message(client.recv(2024), "127.0.0.1"))
