from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
#from tkinter.ttk import *
import time


class Window:
    def __init__(self, width=None, height=None, resizable=True, zoomed=False):
        self.photos = {}
        self.root = Tk()
        if zoomed:
            self.root.state("zoomed")
        if not (width is None and height is None):
            self.root.geometry(f"{width}x{height}")
        self.root.resizable(width=resizable, height=resizable)

    def create_text_label(self,text, root=None):
        if root is None:
            root = self.root
        return Label(root, text=text)

    def create_entry(self, root=None):
        if root is None:
            root = self.root
        return Entry(root)

    def create_text_entry(self, width, height, root=None):
        if root is None:
            root = self.root
        return Text(root, width=width, height=height)

    def create_img_label(self, photo, root = None):
        if root is None:
            root = self.root
        return Label(root, image=self.photos[photo])

    def create_button_label(self, func, root=None, **kwargs):
        if root is None:
            root = self.root
        if "photo" in kwargs.keys():
            kwargs["photo"] = self.photos[kwargs["photo"]]
            kwargs["image"] = kwargs["photo"]
            del kwargs["photo"]
        return Button(root, command=func, **kwargs)

    def update_img_label(self, photo, label, **kwargs):
        label.config(image=self.photos[photo], **kwargs)
        label.update()

    def create_scrollable_frame(self, height, width):
        frame = Frame(self.root)
        canvas = Canvas(frame, width=width, height=height)
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor=NW)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.root.bind("<Configure>", on_frame_configure)

        return frame, inner_frame

    def create_menu_button(self, photo, root=None):
        if root is None:
            root = self.root
        menubutton = Menubutton(root, image=self.photos[photo])
        menubutton.menu = Menu(menubutton, tearoff=0)
        menubutton["menu"] = menubutton.menu
        return menubutton

    def add_button_to_menu(self, menu, text, func):
        menu.menu.add_command(label=text, command=func)

    def remove_button_to_menu(self, menu, button):
        if type(button) == str:
            button = menu.index(button)
        menu.deletecommand(button)

    def add_or_change_photo(self, image, name):
        self.photos[name] = ImageTk.PhotoImage(image)

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

    def locate_widget(self,widget,row,column, **kwargs):
        widget.grid(row=row, column=column, **kwargs)
        widget.update()
        self.root.update()

    def start_function(self, func, ms=0, *args):
        self.root.after(ms, func, args)

    def open_file_dialog(self):
        return filedialog.askopenfilename()

    def update(self):
        self.root.update()

    def start(self):
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()

# def nothing():
#     print("nothing much")
#
# win = Window(1680,1050)
# win.add_or_change_photo(Image.open("default.png"),"default")
# win.add_or_change_photo(Image.open("menu.png"), "menu")
# frame, inner_frame = win.create_scrollable_frame(576, 1036)
# win.locate_widget(frame,0,0)
# menu = win.create_menu_button("menu", inner_frame)
# menu.bind("<Enter>", lambda event : win.locate_widget(menu, event.widget.grid_info()["row"], event.widget.grid_info()["column"], sticky='NE'))
# menu.bind("<Leave>", lambda event: win.remove_widget(menu))
# win.add_button_to_menu(menu,"button", nothing)
# labels = []
# for i in range(20):
#     for j in range(4):
#         labels.append(win.create_img_label("default", inner_frame))
#         win.locate_widget(labels[-1], i,j)
#         labels[-1].bind("<Enter>", lambda event : win.locate_widget(menu, event.widget.grid_info()["row"], event.widget.grid_info()["column"], sticky='NE'))
#         labels[-1].bind("<Leave>", lambda event: win.remove_widget(menu))
# menu.lift()
# win.start()

# def func(entry):
#     print("penis")
#     while True:
#         print(entry.get())
# root = Tk()
# entry = Entry(root)
# entry.grid(row=0,column=0)
# root.after(5000, func, entry)
# root.mainloop()

import threading
import tkinter as tk

class MyThread(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.root = root

    def run(self):
        # Long-running task here
        for i in range(10):
            # Update GUI from the thread using `after`
            self.root.after(1000, self.update_label, i)

    def update_label(self, i):
        label.config(text=str(i))

root = tk.Tk()

label = tk.Label(root, text="")
label.pack()

thread = MyThread(root)
thread.start()

root.mainloop()