import Client

class Student_client(Client):
    def __init__(self, teacher_ip):
        super().__init__(teacher_ip)
        super().open_tcp_connection()

