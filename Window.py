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

    def create_scrollable_frame(self, row, column, width, height, **kwargs):
        container = Frame(width=width, height=height, bg="yellow")
        container.grid(row=row,column=column)
        canvas = Canvas(container, bg="red", width=width, height=height, scrollregion=(0,0,1000,1000))
        canvas.pack(side=LEFT,fill=BOTH)
        vbar = Scrollbar(container, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        frame = Frame(canvas, width=200, height=200, bg="blue")
        frame.grid_propagate()


    def start(self):
        self.root.mainloop()


win = Window(1000,1000)
win.create_scrollable_frame(0,0,600,600)
win.start()


# win = Window()
# win.create_button_label(0,0,lambda: print("button"),"press", )
# label = win.create_img_label(0,1)
# client = TeacherClient()
# win.root.after(5, client.listen_udp, "127.0.0.1", 65410, client.get_img, win.update_img_label, label)
# win.start()