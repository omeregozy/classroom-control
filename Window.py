from tkinter import *
from PIL import ImageTk, Image
import time
from TeacherClient import *


class Window:
    def __init__(self,width=None,height=None,resizable=True,zoomed=False):
        self.photos = {}
        self.root = Tk()
        if zoomed:
            self.root.state("zoomed")
        if not (width is None and height is None):
            self.root.geometry(f"{width}x{height}")
        self.root.resizable(width=resizable, height=resizable)

    def create_img_label(self, row, column, photo, root = None):
        if root is None:
            root = self.root
        label = Label(root, image=self.photos[photo])
        label.grid(row=row, column=column)
        # label.photo_img = self.photos[photo]
        label.update()
        print(label.grid_info())
        return label

    def create_button_label(self, row, column, func,root=None, **kwargs):
        if root is None:
            root = self.root
        if "photo" in kwargs.keys():
            kwargs["photo"] = self.photos[kwargs["photo"]]
        label = Button(root, command=func, **kwargs)
        label.grid(row=row, column=column)
        label.update()

    def update_img_label(self, photo, label, **kwargs):
        label.config(image=self.photos[photo], **kwargs)
        label.update()

    def create_scrollable_frame(self, height, width, row, column, row_span=1, column_span=1):
        frame = Frame(self.root)
        frame.grid(row=row, column=column, rowspan=row_span, columnspan=column_span)
        canvas = Canvas(frame, width=width, height=height,bg="yellow")
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor=NW)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.root.bind("<Configure>", on_frame_configure)

        return inner_frame

    def create_menu_button(self, row, column, photo, root=None):
        if root is None:
            root = self.root
        menubutton = Menubutton(root, image=self.photos[photo])
        menubutton.menu = Menu(menubutton, tearoff=0)
        menubutton["menu"] = menubutton.menu
        menubutton.grid(row=row, column=column)
        return menubutton

    def add_or_change_photo(self, image, name):
        self.photos[name] = ImageTk.PhotoImage(image)

    def add_button_to_menu(self, menu, text, func):
        menu.menu.add_command(label=text, command=func)

    def remove_widget(self, widget, delete=False):
        widget.grid_forget()
        if delete:
            widget.destroy()

    def replace_widget(self,widget1, widget2, delete=False):
        info = widget1.grid_info()
        del info['in']
        widget1.grid_forget()
        if delete:
            widget1.destroy()
        widget2.grid(**info)

    def update(self):
        self.root.update()

    def start(self):
        self.root.mainloop()


win = Window(1680,1050)
frame = win.create_scrollable_frame(576, 1024, 0, 0)
win.add_or_change_photo(Image.open("default.png"),"default")
for i in range(10):
    for j in range(4):
        win.create_img_label(i,j,"default",frame)
#win.add_or_change_photo(Image.open("menu.png"), "menu")
#button = win.create_menu_button(0,0,"menu")
win.start()

# root = Tk()
# img = Image.open("default.png")
# photo_img = ImageTk.PhotoImage(img)
# label = Label(root, image=photo_img)
# label.grid(row=0,column=0)
# root.mainloop()

# root = Tk()
# root.geometry("300x200")
#
# w = Label(root, text='GeeksForGeeks', font="50")
# w.pack()
#
# menubutton = Menubutton(root, text="Menu")
#
# menubutton.menu = Menu(menubutton, tearoff=0)
# menubutton["menu"] = menubutton.menu
#
# var1 = IntVar()
# var2 = IntVar()
# var3 = IntVar()
#
# menubutton.menu.add_checkbutton(label="Courses",
#                                 variable=var1)
# menubutton.menu.add_checkbutton(label="Students",
#                                 variable=var2)
# menubutton.menu.add_checkbutton(label="Careers",
#                                 variable=var3)
#
# menubutton.pack()
# root.mainloop()


# root = Tk()
# image = Image.open("menu.png")
# image.show()
# photo_img = ImageTk.PhotoImage(image)
# menubutton = Menubutton(root, image=photo_img)
# menubutton.menu = Menu(menubutton, tearoff=0)
# menubutton["menu"] = menubutton.menu
# menubutton.grid(row=0, column=0)
# root.mainloop()