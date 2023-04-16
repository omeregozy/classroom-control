from Server import Server


class TeacherServer(Server):
    def __init__(self):
        super().__init__()
        super().open_tcp()
        super().open_multicast()
        self.streaming = None

    def student_start_stream(self, client):
        if self.streaming is not None:
            self.streaming.send("close stream".encode())
        else:
            super().send_tcp_to_all("start listening",client)
        self.streaming = client
        client.send("start streaming")

    def new_lesson(self):
        self.send_tcp_to_all(b"new lesson")

