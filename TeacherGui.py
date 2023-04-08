from Window import Window
from TeacherServer import TeacherServer
from TeacherClient import TeacherClient
from PIL import Image

class TeacherGui(Window):
    def __init__(self):
        super().__init__(1680, 1050, False)
        self.server = TeacherServer()
        self.client = TeacherClient()
        self.add_or_change_photo(Image.open("default.png"), "default")
        self.add_or_change_photo(Image.open("menu.png"), "menu")
        self.screens_frame, self.screens_inner_frame = self.create_scrollable_frame(576, 1036)
        self.locate_widget(self.screens_frame, 1, 0, columnspan=4)
        self.screen_menu = self.create_menu_button("menu", self.screens_inner_frame)
        self.new_lesson_button = self.create_button_label(self.server.new_lesson, text = "start a new lesson")
        self.shut_off_screens_button = self.create_button_label(self.server.shut_off_screens, text = "shut off screens")
        self.shut_off_computers_button = self.create_button_label(self.server.shut_off_computers, text = "shut off computers")
        self.block_screens_button = self.create_button_label(self.server.block_screens, text = "block screens")
        self.send_message_button = self.create_button_label(self.server.new_lesson, text = "send a message / file")

    def send_message(self):
        self.root.geometry("1880x1050")
        self.


