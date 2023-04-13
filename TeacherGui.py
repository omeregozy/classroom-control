from Window import Window
from TeacherServer import TeacherServer
from TeacherClient import TeacherClient
from PIL import Image
import zipfile
from io import BytesIO

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
        self.send_message_button = self.create_button_label(self.send_message(), text = "send a message / file")

    def send_message(self):
        win = Window()
        zip_data = BytesIO()
        list_of_labels = []
        zip_file = zipfile.ZipFile(zip_data, mode='w')
        label = win.create_text_label("write your comment")
        win.locate_widget(label, 2, 0)
        comment = win.create_text_entry(20,5)
        win.locate_widget(comment, 3, 0)
        def send():
            self.server.send_tcp_to_all(comment.get().encode())
            zip_file.close()
            self.server.send_tcp_to_all(zip_data.getvalue())
        send_button = win.create_button_label(send, text="send")
        win.locate_widget(send_button, 4, 0)
        win.create_scrollable_frame(50,20)
        def choose_file_and_show():
            file_name = win.open_file_dialog()
            file_arc_name = file_name.split('/')[-1]
            zip_file.write(file_name, file_arc_name)
            list_of_labels.append(win.create_text_label(file_arc_name))
            location = len(list_of_labels)
            win.locate_widget(list_of_labels[-1], location)
            win.update()
        choose_file_button = win.create_button_label(choose_file_and_show, text="choose_file")
        win.locate_widget(choose_file_button, 0, 0)





win = TeacherGui()
win.start()