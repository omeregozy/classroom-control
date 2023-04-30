import socket
import struct
import select
import threading
import time

TCP_PORT = 5060
UDP_PORT = 5070
MULTICAST_PORT = 5080
MULTICAST_GROUP = "224.0.0.151"


class Server:
    def __init__(self):
        self.tcp_server = None
        self.udp_server = None
        self.multicast_server = None
        self.multicast_port = MULTICAST_PORT
        self.udp_port = UDP_PORT
        self.multicast_ip = MULTICAST_GROUP
        self.clients_list = []

    def open_tcp(self):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind((socket.gethostname(), TCP_PORT))

    def open_udp(self):
        self.udp_server = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)

    def open_multicast(self):
        self.multicast_port = MULTICAST_PORT
        self.multicast_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multicast_server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)

    def listen_tcp(self, buffer_size, handle_new_client, handle_msg, handle_close):
        if self.tcp_server is None:
            self.open_tcp()
        sockets_list = [self.tcp_server]
        sockets_list.extand(self.clients_list)
        while True:
            read_sockets, _, _ = select.select(sockets_list, [], [])
            for sock in read_sockets:
                if sock == self.tcp_server:
                    client_sock, client_address = sock.accept()
                    sockets_list.append(client_sock)
                    self.clients_list.append(client_sock)
                    handle_new_client(client_sock)
                else:
                    try:
                        data = sock.recv(buffer_size)
                        if data:
                            handle_msg(client_sock, data)
                        else:
                            handle_close(sock)
                            sock.close()
                            sockets_list.remove(sock)
                            self.clients_list.remove(sock)
                    except:
                        handle_close(sock)
                        sock.close()
                        sockets_list.remove(sock)
                        self.clients_list.remove(sock)

    def send_multicast(self, msg):
        self.multicast_server.sendto(msg, (self.multicast_ip, self.multicast_port))

    def send_udp(self, ip, msg):
        self.udp_server.sendto(msg, (ip, self.udp_port))

    def send_tcp_to_all(self, msg, not_to=[]):
        for i in self.clients_list:
            if i not in not_to:
                self.i.send(msg)

server = Server()
server.open_multicast()
for i in range(1000):
    time.sleep(0.1)
    server.send_multicast(str(i).zfill(3).encode())