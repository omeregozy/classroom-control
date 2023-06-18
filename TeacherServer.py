from Server import Server
from multiprocessing import Process, Pipe
import win32gui
from io import BytesIO
from PIL import ImageGrab, Image
import threading
import select


send = True

def stop(conn):
    conn.recv_bytes()
    global send
    send = False

def get_screenshots(conn):
    cursor = Image.open("cursor.png")
    threading.Thread(target=stop, args=[conn]).start()
    bio = BytesIO()
    quality = 95
    while send:
        img = ImageGrab.grab()
        img = img.convert("RGBA")
        cursor_pos = win32gui.GetCursorPos()
        img.alpha_composite(cursor, dest=(cursor_pos[0], cursor_pos[1]))
        img = img.convert("RGB")
        length = 65409
        while length > 65408:
            img.save(bio, "JPEG", quality=quality)
            bio.seek(0)
            img_file = bio.getvalue()
            bio.truncate(0)
            length = len(img_file)
            if length < 65398:
                conn.send_bytes(str(len(img_file)).zfill(10).encode() + img_file[::-1].zfill(65398)[::-1])
                if quality < 95 and length < 55000:
                    quality += 5
            else:
                quality -= 5


class TeacherServer(Server):
    def __init__(self, encryption):
        super().__init__()
        super().open_tcp()
        super().open_multicast()
        self.tcp_server.settimeout(5)
        self.streaming = None
        self.conn = None
        self.encryption = encryption

    def listen_tcp(self, buffer_size, handle_new_client, handle_close):
        if self.tcp_server is None:
            self.open_tcp()
        sockets_list = [self.tcp_server]
        sockets_list.extend(self.clients_list)
        while True:
            read_sockets, _, _ = select.select(sockets_list, [], [],1)
            for sock in read_sockets:
                if sock == self.tcp_server:
                    client_sock, client_address = sock.accept()
                    try:
                        print("student")
                        self.encryption.add_student(client_address, client_sock.recv(450))
                        sockets_list.append(client_sock)
                        self.clients_list.append(client_sock)
                        handle_new_client(client_sock)
                    except:
                        client_sock.close()
                else:
                    try:
                        sock.recv(buffer_size)
                    except:
                        handle_close(sock)
                        sock.close()
                        sockets_list.remove(sock)
                        self.clients_list.remove(sock)
    def send_tcp_to_all(self, msg, not_to = []):
        for i in self.clients_list:
            if i not in not_to:
                i.send(self.encryption.encrypt_message(msg,i.getsockname()))

    def send_tcp(self, client, msg):
        client.send(self.encryption.encrypt_message(msg, client.getsockname()))

    def send_full_screen(self, client):
        self.send_tcp(client, b"full screen")

    def send_normal_screen(self, client):
        self.send_tcp(client, b"normal screen")

    def send_coordinates(self, client, x, y):
        self.send_tcp(client, f"({x},{y})".encode())

    def send_press(self,client,num):
        self.send_tcp(client,f"press {num}".encode())
    def send_release(self,client,num):
        self.send_tcp(client, f"release press {num}".encode())

    def blackout(self, client):
        self.send_tcp(client,b"black out")

    def release_blackout(self,  client):
        self.send_tcp(client, b"release black out")

    def stream_student(self, client):
        if self.streaming is None:
            self.send_tcp_to_all(b"start listening", [client])
        self.streaming = client
        self.send_tcp(client,b"stream")

    def release_stream(self):
        if self.streaming is self:
            self.conn.send_bytes(b"stop")
            self.conn = None
        else:
            self.send_tcp(self.streaming,b"release stream")
        self.send_tcp_to_all(b"stop listening", [self.streaming])
        self.streaming = None

    def stream_screen(self):
        def send_screenshots():
            while self.streaming is self:
                self.send_multicast(self.conn.recv_bytes())
            self.send_tcp_to_all(b"stop listening")
        if self.streaming is None:
            self.send_tcp_to_all(b"start listening")
        self.streaming = self
        self.conn, conn = Pipe(duplex=True)
        Process(target=get_screenshots, args=[conn]).start()
        threading.Thread(target=send_screenshots).start()



