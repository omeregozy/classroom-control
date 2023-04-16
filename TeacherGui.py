from Window import Window
from TeacherServer import TeacherServer
from TeacherClient import TeacherClient
from PIL import Image
import zipfile
from io import BytesIO

def do_nothing():
    print("nothing")
class TeacherGui(Window):
    def __init__(self):
        super().__init__(1680, 1050, False)
        self.server = TeacherServer()
        self.client = TeacherClient()
        self.add_or_change_photo(Image.open("default.png"), "default")
        self.add_or_change_photo(Image.open("menu.png"), "menu")
        self.screens_frame, self.screens_inner_frame = self.create_scrollable_frame(576, 1036)
        self.screen_menu = self.create_menu_button("menu", self.screens_inner_frame)
        # self.new_lesson_button = self.create_button_label(self.server.new_lesson, text = "start a new lesson")
        # self.shut_off_screens_button = self.create_button_label(self.server.shut_off_screens, text = "shut off screens")
        # self.shut_off_computers_button = self.create_button_label(self.server.shut_off_computers, text = "shut off computers")
        # self.block_screens_button = self.create_button_label(self.server.block_screens, text = "block screens")
        # self.send_message_button = self.create_button_label(self.send_message, text = "send a message / file")
        self.buttons = []
        self.buttons.append(self.create_button_label(do_nothing, text="start a new lesson"))
        self.buttons.append(self.create_button_label(do_nothing, text="shut off screens"))
        self.buttons.append(self.create_button_label(do_nothing,text="shut off computers"))
        self.buttons.append(self.create_button_label(do_nothing, text="block screens"))
        self.buttons.append(self.create_button_label(self.send_message, text="send a message / file"))
        for i in range(len(self.buttons)):
            self.locate_widget(self.buttons[i],0,i)
        self.locate_widget(self.screens_frame, 1, 0, columnspan=len(self.buttons)) 


    def send_message(self):
        win = Window()
        zip_data = BytesIO()
        list_of_labels = []
        zip_file = zipfile.ZipFile(zip_data, mode='w')
        label = win.create_text_label("write your comment")
        win.locate_widget(label, 2, 0)
        comment = win.create_text_entry(40,10)
        win.locate_widget(comment, 3, 0)
        def send():
            win.destroy()
            self.server.send_tcp_to_all(comment.get('1.0', 'end-1c').encode())
            zip_file.close()
            self.server.send_tcp_to_all(zip_data.getvalue())
        send_button = win.create_button_label(send, text="send")
        win.locate_widget(send_button, 4, 0)
        frame, inner_frame = win.create_scrollable_frame(100,300)
        win.locate_widget(frame,1,0)
        def choose_file_and_show():
            file_name = win.open_file_dialog()
            file_arc_name = file_name.split('/')[-1]
            print(file_name)
            zip_file.write(file_name, file_arc_name)
            print(file_name)
            list_of_labels.append(win.create_text_label(file_arc_name, inner_frame))
            location = len(list_of_labels) - 1
            win.locate_widget(list_of_labels[-1], location, 0)
            win.update()
        choose_file_button = win.create_button_label(choose_file_and_show, text="choose_file")
        win.locate_widget(choose_file_button, 0, 0)






win = TeacherGui()
win.start()