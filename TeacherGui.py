from Window import Window
from TeacherServer import TeacherServer
from TeacherClient import TeacherClient
from PIL import Image
import zipfile
from io import BytesIO
import threading


def do_nothing():
    print("nothing")


class TeacherGui(Window):
    def __init__(self):
        super().__init__(1056, 626, False)
        self.server = TeacherServer()
        self.client = TeacherClient()
        self.add_or_change_photo(Image.open("default.png"), "default")
        self.add_or_change_photo(Image.open("menu.png"), "menu")
        self.screens_frame, self.screens_inner_frame = self.create_scrollable_frame(576, 1036)
        self.buttons = []
        self.buttons.append(self.create_button_label(do_nothing, text="blackout all screens"))
        self.buttons.append(self.create_button_label(do_nothing, text="broadcast your screen"))
        self.buttons.append(self.create_button_label(self.send_message, text="send a message / file"))
        for i in range(len(self.buttons)):
            self.locate_widget(self.buttons[i],0,i)
        self.locate_widget(self.screens_frame, 1, 0, columnspan=len(self.buttons))
        self.ip_to_screen_and_menu = {}
        self.big_screen_addr = None
        self.big_screen_client = None
        self.add_or_change_photo(Image.open("default.png"), "default")
        self.big_screen = self.create_img_label("default")
        def send_location(event):
            self.big_screen_client.send(f"({event.x},{event.y})".zfill(20).encode())
        def send_press(event):
            self.big_screen_client.send(f"press {event.num}".zfill(20).encode())
        def send_release(event):
            self.big_screen_client.send(f"release {event.num}".zfill(20).encode())
        def start_controlling_mouse(event):
            self.server.control(self.big_screen_client)
            self.big_screen.unbind("<Button>")
            self.big_screen.bind("<Motion>", send_location)
            self.big_screen.bind("<Button>", send_press)
            self.big_screen.bind("<ButtonRelease>", send_release)

        def stop_controlling_mouse(event):
            self.big_screen.unbind_all()
            self.big_screen.bind("<Button>", start_controlling_mouse)
            self.server.release_control(self.big_screen_client)
        self.big_screen.bind("<Button>", start_controlling_mouse)
        self.big_screen.bind("<Leave>", stop_controlling_mouse)
    def handle_new_student(self, client):
        addr = client.getpeername()[0]
        if addr not in self.ip_to_screen_and_menu:
            menu = self.create_menu_button("menu", self.screens_inner_frame)
            screen = self.create_img_label("default", self.screens_inner_frame)
            screen.bind("<Enter>", lambda event: self.display_menu(event, menu))
            hide = lambda event: self.hide_menu(event, menu, screen)
            screen.bind("<Leave>", hide)
            menu.bind("<Leave>", hide)
            self.ip_to_screen_and_menu[addr] = (screen, menu)
            self.locate_widget(screen, len(self.ip_to_screen) % 4 - 1, int(len(self.ip_to_screen) / 4 - 1))
            self.ip_to_screen_and_menu[addr] = screen, menu
        else:
            menu = self.ip_to_screen_and_menu[addr][1]
        old_screen_and_menu = self.ip_to_screen_and_menu[addr]
        def control():
            self.ip_to_screen_and_menu[addr] = self.one_screen, None
            self.big_screen_addr = addr
            self.big_screen_client = client
            self.replace_widget(self.screens_frame, self.big_screen)
        self.add_button_to_menu(menu, "control")


    def send_message(self, func=None):
        if func is None:
            func = self.server.send_tcp_to_all
        win = Window()
        zip_data = BytesIO()
        list_of_labels = []
        zip_file = zipfile.ZipFile(zip_data, mode='w')
        label = win.create_text_label("write your comment")
        win.locate_widget(label, 2, 0)
        comment = win.create_text_entry(40,10)
        win.locate_widget(comment, 3, 0)

        def send():
            func(comment.get('1.0', 'end-1c').encode())
            zip_file.close()
            func(zip_data.getvalue())
            win.destroy()
        send_button = win.create_button_label(send, text="send")
        win.locate_widget(send_button, 4, 0)
        frame, inner_frame = win.create_scrollable_frame(100,300)
        win.locate_widget(frame,1,0)

        def choose_file_and_show():
            file_name = win.open_file_dialog()
            file_arc_name = file_name.split('/')[-1]
            zip_file.write(file_name, file_arc_name)
            list_of_labels.append(win.create_text_label(file_arc_name, inner_frame))
            location = len(list_of_labels) - 1
            win.locate_widget(list_of_labels[-1], location, 0)
            win.update()
        choose_file_button = win.create_button_label(choose_file_and_show, text="choose_file")
        win.locate_widget(choose_file_button, 0, 0)

    def display_screens(self):
        def display_img(addr):
            if addr not in self.ip_to_screen_and_menu:
                menu = self.create_menu_button("menu", self.screens_inner_frame)
                screen = self.create_img_label(addr, self.screens_inner_frame)
                screen.bind("<Enter>", lambda event : self.display_menu(event, menu))
                hide = lambda event : self.hide_menu(event, menu, screen)
                screen.bind("<Leave>", hide)
                menu.bind("<Leave>", hide)
                self.ip_to_screen_and_menu[addr] = (screen, menu)
                self.locate_widget(screen, len(self.ip_to_screen)%4 - 1, int(len(self.ip_to_screen)/4 -1))
                self.ip_to_screen_and_menu[addr] = screen, menu
            else:
                self.update_img_label(addr, self.ip_to_screen_and_menu[addr][0])

        def handle_img(addr, img):
            if self.one_screen_addr is not None and self.one_screen_addr != addr:
                return
            self.add_or_change_photo(img, addr)
            self.start_function(display_img, 0, addr)

        t = threading.Thread(target=self.client.listen_udp, args=[65410, self.client.get_img, handle_img])
        t.start()

    def display_streaming_screen(self):
        def display_img()
        def handle_img(addr, img):
            if self.one_screen_addr is not None and self.one_screen_addr != addr:
                return
            self.add_or_change_photo(img, addr)
            self.start_function(display_img, 0, addr)

        t = threading.Thread(target=self.client.listen_udp, args=[65410, self.client.get_img, handle_img])
        t.start()
    def display_menu(self, event, menu):
        info = event.widget.grid_info()
        self.locate_widget(menu, info["row"], info["column"], anchor="ne")

    def hide_menu(self, event, menu, screen):
        if event.widget is not menu or screen:
            self.remove_widget(menu)


if __name__ == "__main__":
    win = TeacherGui()
    win.display_screens()
    win.start()
