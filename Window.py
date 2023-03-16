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

    def create_scrollable_frame(self, height, width, row, column, **kwargs):
        container = Frame(self.root, height=height, width=width,bg="yellow")
        container.grid(row=row, column=column)
        canvas = Canvas(container,relief="raised",bg="red")
        frame = Frame(canvas, height=1000, width=20,bg="blue")
        v = Scrollbar(container, orient='vertical', command=canvas.yview, height=height)
        canvas.config(yscrollcommand=v.set)
        canvas.grid(row=0,column=0)
        v.grid(row=0,column=1)
        frame.grid(row=0, column=0)
        canvas.create_window(25,25,window=frame)
        canvas.configure(scrollregion=canvas.bbox("all"))



    def start(self):
        self.root.mainloop()


win = Window(1000,1000)
win.create_scrollable_frame(200,200,0,0)
win.start()


# win = Window()
# win.create_button_label(0,0,lambda: print("button"),"press", )
# label = win.create_img_label(0,1)
# client = TeacherClient()
# win.root.after(5, client.listen_udp, "127.0.0.1", 65410, client.get_img, win.update_img_label, label)
# win.start()