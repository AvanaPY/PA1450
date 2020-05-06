import tkinter as tk

BIG_FONT = ('Helvetica', 18)

WINDOW_SIZES = (
    '640x480', '800x600', '960x720', '1024x768',  # 4:3 
    '1024x576', '1152x648', '1280x720', '1600x900', '1920x1080' # 16:9
)
DEFAULT_SIZE = '1280x720'

class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        label = tk.Label(self, text='Visualizing data', font=BIG_FONT).pack()
        self.pack()

        menu = tk.Menu(parent)
        controller.config(menu=menu)

        _file = tk.Menu(menu)
        _file.add_command(label='Exit', command=controller.client_exit)
        menu.add_cascade(label='File', menu=_file)

        _resize = tk.Menu(menu)
        for size in WINDOW_SIZES:
            _resize.add_command(label=size, command=self.ResizeCommand(controller, size))
        menu.add_cascade(label='Resize', menu=_resize)

    class ResizeCommand:
        def __init__(self, controller, size):
            self.controller = controller
            self.size = size
        def __call__(self):
            self.controller.set_size(self.size)

START_FRAME = Page
PAGES = (Page, )