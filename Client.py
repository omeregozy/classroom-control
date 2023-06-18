import socket
import struct
import random
import threading
import time
TCP_PORT = 5060
UDP_PORT = 5070
MULTICAST_PORT = 5080
MULTICAST_GROUP = "224.0.0.151"


class Client:
    def __init__(self, remote_ip=None):
        self.tcp_client = None
        self.tcp_server = None
        self.udp_client = None
        self.multicast_client = None
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.remote_ip = remote_ip[0]
        self.multicast_port = MULTICAST_PORT
        self.udp_port = UDP_PORT
        self.tcp_port = TCP_PORT
        self.multicast_ip = MULTICAST_GROUP

    def listen_udp(self, buffer_size, handle_msg, *args):
        if self.udp_client is None:
            self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_client.bind((socket.gethostbyname(socket.gethostname()), self.udp_port))
        while True:
            data, addr = self.udp_client.recvfrom(buffer_size)
            handle_msg(data, addr[0], *args)

    def listen_multicast(self, buffer_size, handle_msg, *args):
        if self.multicast_client is None:
            self.multicast_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.multicast_client.bind(("", self.multicast_port))
            group = socket.inet_aton(self.multicast_ip)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.multicast_client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data, addr = self.multicast_client.recvfrom(buffer_size)
            if addr[0] != socket.gethostbyname(socket.gethostname()):
                handle_msg(data, addr[0], *args)

    def open_tcp_connection(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((self.remote_ip, self.tcp_port))
        self.tcp_client.connect((self.remote_ip, self.tcp_port))

    def listen_tcp(self, buffer_size, handle_msg):
        if self.tcp_client is None:
            self.open_tcp_connection()
        while True:
            handle_msg(self.tcp_client.recv(buffer_size))
