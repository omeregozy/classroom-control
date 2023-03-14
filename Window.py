from tkinter import *
from PIL import ImageTk, Image
import time
from TeacherClient import *


class Window:
    def __init__(self,width=None,height=None):
        self.root = Tk()
        if not (width is None and height is None):
            self.root.geometry(f"{width}x{height}")
        self.root.resizable(width=False, height=False)

    def create_img_label(self, row, column, image="default.png", root = None):
        if root is None:
            root = self.root
        if type(image) == str:
            image = Image.open(image)
        print(image)
        image.thumbnail((200,200))
        image = ImageTk.PhotoImage(image)
        label = Label(root, image=image)
        label.grid(row=row, column=column)
        label.update()
        return label

    def create_button_label(self, row, column, func, text,root=None, **kwargs):
        if root is None:
            root = self.root
        label = Button(root, command=func, text=text, **kwargs)
        label.grid(row=row, column=column)
        label.update()

    def update_img_label(self, img, label, **kwargs):
        if img == None:
            label.config(**kwargs)
            return
        img = ImageTk.PhotoImage(img)
        label.config(image=img, **kwargs)
        label.update()
        self.root.update()

    def create_scrollable_frame(self, text, row, column, **kwargs):
        canvas = Canvas
        label_frame = LabelFrame(canvas, text=text)
        label_frame.grid(row,column)


    def start(self):
        self.root.mainloop()


win = Window()


# win = Window()
# win.create_button_label(0,0,lambda: print("button"),"press", )
# label = win.create_img_label(0,1)
# client = TeacherClient()
# win.root.after(5, client.listen_udp, "127.0.0.1", 65410, client.get_img, win.update_img_label, label)
# win.start()