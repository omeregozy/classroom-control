from Window import Window
import threading
import win32gui
import win32con
import win32api
import time
import queue
from StudentClient import StudentClient
from StudentServer import StudentServer
from StudentEncryption import StudentEncryption

class StudentGui(Window):
    def __init__(self, stream_or_blackout, client=None):
        self.client = client
        super().__init__(resizable=False,title="full screen student program")
        def disable_close():
            pass
        self.root.protocol("WM_DELETE_WINDOW", disable_close)
        self.root.attributes("-fullscreen", True)
        self.root["bg"] = "black"
        self.window_exist = True
        if stream_or_blackout == "stream":
            self.start_function(self.show_stream, 5)
        elif stream_or_blackout == "blackout":
            self.blackout()
        else:
            self.close()
        self.start_function(self.remain_in_the_front,5)

    def remain_in_the_front(self):
        def check_if_in_the_front():
            HWND = win32gui.FindWindow(None, "full screen student program")
            while self.window_exist:
                if win32gui.GetForegroundWindow() != HWND:
                    win32gui.ShowWindow(HWND, win32con.SW_RESTORE)
                    win32gui.SetWindowPos(HWND, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                          win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                    win32gui.SetActiveWindow(HWND)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    time.sleep(0.005)
        threading.Thread(target=check_if_in_the_front).start()

    def close(self):
        self.window_exist = False
        time.sleep(0.5)
        self.start_function(self.destroy, 0)

    def show_stream(self):
        label = self.create_img_label("default")
        label.pack()
        def show_photo(img):
            self.add_or_change_photo(img, "stream")
            self.start_function(self.update_img_label, 0, "stream", label)
        threading.Thread(target=client.listen_multicast, args=(64998, self.client.get_image, show_photo)).start()

    def blackout(self):
        label = self.create_text_label("QUIET", bg="black", fg="white", font=("Calibari", 100))
        label.place(relx=0.4, rely=0.4)

def check_when_to_close_window(queue, window):
    data = queue.get()
    if data == "close":
        window.close()

if __name__ == "__main__":
    client_queue = queue.Queue()
    encryption = StudentEncryption()
    client = StudentClient(client_queue, encryption)
    server = StudentServer(client.remote_ip, encryption)
    client.add_server(server)
    threading.Thread(target=client.listen_tcp, args=[16,client.listen_to_teacher]).start()
    threading.Thread(target=server.send_screenshots).start()
    while not client.tcp_client.closed:
        data = queue.get()
        window = StudentGui(data)
        threading.Thread(target=check_when_to_close_window, args=[queue, window])
        window.start()


