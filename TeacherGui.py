from Window import Window
from TeacherServer import TeacherServer
from TeacherClient import TeacherClient
from PIL import Image
import threading
from TeacherEncryption import TeacherEncryption


def do_nothing():
    print("nothing")


class TeacherGui(Window):
    def __init__(self):
        super().__init__(1056, 626, False)
        self.encryption = TeacherEncryption()
        self.server = TeacherServer(self.encryption)
        self.client = TeacherClient(self.encryption)
        self.add_or_change_photo(Image.open("default.png"), "default")
        self.add_or_change_photo(Image.open("menu.png"), "menu")
        self.screens_frame, self.screens_inner_frame = self.create_scrollable_frame(576, 1036)
        self.buttons = []
        self.buttons.append(self.create_button_label(self.server.blackout_all(), text="blackout all screens"))
        self.buttons.append(self.create_button_label(do_nothing, text="broadcast your screen"))
        for i in range(len(self.buttons)):
            self.locate_widget(self.buttons[i],0,i)
        self.locate_widget(self.screens_frame, 1, 0, columnspan=len(self.buttons)+1)
        self.ip_to_screen_and_menu = {}
        self.big_screen_addr = None
        self.big_screen_client = None
        self.add_or_change_photo(Image.open("default.png"), "default")
        self.big_screen = self.create_img_label("default")
        self.big_screen_addr = None

        def send_location(event):
            self.server.send_coordinates(self.big_screen_client,event.x,event.y)

        def send_press(event):
            self.server.send_press(self.big_screen_client,event.num)

        def send_release(event):
            self.server.send_release(self.big_screen_client,event.num)

        def start_controlling_mouse(event):
            self.big_screen.unbind("<Button>")
            self.big_screen.bind("<Motion>", send_location)
            self.big_screen.bind("<Button>", send_press)
            self.big_screen.bind("<ButtonRelease>", send_release)

        def stop_controlling_mouse(event):
            self.big_screen.unbind_all("All")
            self.big_screen.bind("<Button>", start_controlling_mouse)

        self.big_screen.bind("<Button>", start_controlling_mouse)
        self.big_screen.bind("<Leave>", stop_controlling_mouse)
        self.display_screens(self.client.listen_udp, True)
        self.display_screens(self.client.listen_multicast, False)
        threading.Thread(target=self.server.listen_tcp, args=(16, self.handle_new_student, self.remove_student)).start()

    def handle_new_student(self, client):
        addr = client.getpeername()[0]
        if addr not in self.ip_to_screen_and_menu:
            screen = self.create_img_label("default", self.screens_inner_frame)
            menu = self.create_menu_button("menu", self.screens_inner_frame)
            screen.bind("<Enter>", lambda event: self.display_menu(event, menu))
            hide = lambda event: self.hide_menu(event, menu, screen)
            screen.bind("<Leave>", hide)
            menu.bind("<Leave>", hide)
            self.ip_to_screen_and_menu[addr] = (screen, menu)
            self.locate_widget(screen, len(self.ip_to_screen_and_menu) % 4 - 1, int(len(self.ip_to_screen_and_menu) / 4 - 1))
            self.ip_to_screen_and_menu[addr] = screen, menu
        else:
            menu = self.ip_to_screen_and_menu[addr][1]

        main_screen_and_menu = self.ip_to_screen_and_menu[addr]

        def return_to_shared_screen():
            self.server.send_normal_screen(self.big_screen_client)
            self.ip_to_screen_and_menu[addr] = main_screen_and_menu
            self.replace_widget(self.big_screen,self.screens_frame)
            self.big_screen_addr = addr
            self.big_screen_client = client


        def control(make_button=True):
            self.ip_to_screen_and_menu[addr] = self.big_screen, None
            self.big_screen_addr = addr
            self.big_screen_client = client
            self.replace_widget(self.screens_frame, self.big_screen)
            self.server.send_full_screen(self.big_screen_client)
            if make_button:
                button = self.create_button_label(return_to_shared_screen,text="release control")
                self.locate_widget(button, 0, len(self.buttons))

        def start_streaming():
            self.server.stream_student(client)
            control()
            return_to_shared_screen_and_release_stream = lambda a : (return_to_shared_screen(), self.server.release_stream())
            button = self.create_button_label(return_to_shared_screen_and_release_stream, text="release stream")
            self.locate_widget(button, 0, len(self.buttons))


        def blackout():
            self.server.blackout(client)
            self.change_button_in_menu(menu, "blackout", "release blackout", release_blackout)

        def release_blackout():
            self.server.release_blackout(client)
            self.change_button_in_menu(menu, "release blackout", "blackout", blackout)

        self.add_button_to_menu(menu, "control", control)
        self.add_button_to_menu(menu, "stream", start_streaming)
        self.add_button_to_menu(menu, "blackout", blackout)

    def display_screens(self, streaming_func, decrypt):
        def display_img(addr):
            if addr not in self.ip_to_screen_and_menu:
                #self.ip_to_screen_and_menu[addr] = None
                screen = self.create_img_label(addr, self.screens_inner_frame)
                menu = self.create_menu_button("menu", self.screens_inner_frame)
                screen.bind("<Enter>", lambda event : self.display_menu(event, menu))
                hide = lambda event : self.hide_menu(event, menu, screen)
                screen.bind("<Leave>", hide)
                menu.bind("<Leave>", hide)
                self.ip_to_screen_and_menu[addr] = (screen, menu)
                self.locate_widget(screen, len(self.ip_to_screen_and_menu)%4 - 1, int(len(self.ip_to_screen_and_menu)/4 -1))
                self.ip_to_screen_and_menu[addr] = screen, menu
            else:
                self.update_img_label(addr, self.ip_to_screen_and_menu[addr][0])

        def handle_img(addr, img):
            if self.big_screen_addr is not None and self.big_screen_addr != addr:
                return
            if img.size[0] > 1024:
                img.thumbnail((1024, 576))
            self.add_or_change_photo(img, addr)
            self.start_function(display_img, 0, addr)

        t = threading.Thread(target=streaming_func, args=[65408, self.client.get_img, handle_img, decrypt])
        t.start()

    def display_menu(self, event, menu):
        print("display")
        info = event.widget.grid_info()
        self.locate_widget(menu, info["row"], info["column"], sticky="ne")

    def hide_menu(self, event, menu, screen):
        print("hide")
        x, y = self.root.winfo_pointerxy()
        widget_under_mouse = self.root.winfo_containing(x, y)
        if widget_under_mouse is not menu and widget_under_mouse is not screen:
            self.remove_widget(menu)

    def remove_student(self, sock):
        for i in self.ip_to_screen_and_menu[sock.getsockname()]:
            self.remove_widget(i, True)

if __name__ == "__main__":
    win = TeacherGui()
    win.start()
