import socket


TCP_PORT = 5060
UDP_PORT = 5070
MULTICAST_PORT = 5080
MULTICAST_GROUP = "?.?.?.?"

class Client:
    def __init__(self):
        self.tcp_server = None
        self.udp_client = None
        self.multicast_client = None
        self.multicast_port = MULTICAST_PORT
        self.udp_port = UDP_PORT
        self.multicast_ip = MULTICAST_GROUP

    def listen_udp(self, ip, buffer_size, handle_msg, *args):
        if self.udp_client is None:
            self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_client.bind((ip, self.udp_port))
        while True:
            data, addr = self.udp_client.recvfrom(buffer_size)
            handle_msg(data, *args)

    def listen_multicast(self, handle_msg):
        pass
    def listen_tcp(self, handle_msg):
        pass
    def send_tcp(self):
        pass


