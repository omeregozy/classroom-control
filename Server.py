import socket
import threading
import

TCP_PORT = 5060
UDP_PORT = 5070
MULTICAST_PORT = 5080
MULTICAST_GROUP = "?.?.?.?"


class Server:
    def __init__(self):
        self.tcp_server = None
        self.udp_server = None
        self.multicast_server = None
        self.multicast_port = MULTICAST_PORT
        self.udp_port = UDP_PORT
        self.multicast_ip = MULTICAST_GROUP
        self.clients_list = []

    def open_tcp(self, handle_client, *args):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind((socket.gethostname(), TCP_PORT))
        threading.Thread(target=Server.connect_tcp, args=(self, handle_client))

    def open_udp(self):
        self.udp_port = UDP_PORT
        self.udp_server = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)

    def open_multicast(self):
        self.multicast_port = MULTICAST_PORT
        self.multicast_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multicast_server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)

    def connect_tcp(self, handle_client):
        while True:
            client, address = self.tcp_server.accept()
            self.clients_list.append(client)
            threading.Thread(target=handle_client, args=(self, client)).run()

    def send_multicast(self, msg):
        self.multicast_server.sendto(msg, (self.multicast_ip, self.multicast_port))

    def send_udp(self, ip, msg):
        self.udp_server.sendto(msg, (ip, self.udp_port))

    def send_tcp_to_all(self, msg, not_to=[]):
        for i in self.clients_list:
            if i not in not_to:
                self.i.send(msg)
