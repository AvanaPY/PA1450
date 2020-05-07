import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import animation as animation
import matplotlib.pyplot as plt

from matplotlib import style
style.use('ggplot')

import tkinter as tk
import data_manager
import datetime
import math

BIG_FONT = ('Helvetica', 18)
MEDIUM_FONT = ('Helvetica', 14)
SMALL_FONT = ('Helvetica', 8)

WINDOW_SIZES = (
    '640x480', '800x600', '960x720', '1024x768',  # 4:3 
    '1024x576', '1152x648', '1280x720', '1600x900', '1920x1080' # 16:9
)
DEFAULT_SIZE = '1280x720'

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, bg='white')
        label = tk.Label(self, text='Visualizing data', bg='white', font=BIG_FONT).pack()
        
        #########################################
        # Menu related things

        menu = tk.Menu(parent)
        controller.config(menu=menu)

        # File related
        _file = tk.Menu(menu)
        _file.add_command(label='Exit', command=controller.client_exit)
        menu.add_cascade(label='File', menu=_file)

        # Resize the window buttons
        _resize = tk.Menu(menu)
        for size in WINDOW_SIZES:
            _resize.add_command(label=size, command=self.ResizeCommand(controller, size))
        menu.add_cascade(label='Resize', menu=_resize)

        # Attribute related

        _attributes = tk.Menu(menu)
        for data_name in data_manager.WEATHER_PAIRS:
            _attributes.add_command(label=data_name, command=self.LoadDataCommand(self, data_name))
        menu.add_cascade(label='Attributes', menu=_attributes)

        self._figure = Figure(figsize=(5, 5), dpi=100)
        self._plot = self._figure.add_subplot(111)

        self._graph_canvas = FigureCanvasTkAgg(self._figure, self)
        self._graph_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def plot_data(self, dataframe, label, color='red'):

        count = dataframe.shape[0]
        self._plot.set_title(f'Plotting {label}')
        
        self._plot.clear()
        self._plot.set_xlabel('Time')
        self._plot.set_xticks([])
        self._plot.set_ylabel('Value', rotation=90)
        self._plot.plot(range(count), dataframe['Value'], label=label, color=color)
        self._plot.legend()

        self._graph_canvas.draw()

    def load_data(self, data_name, min_date=None, max_date=None):
        data = data_manager.load_data(data_name)
        if min_date or max_date:
            data = data_manager.get_interval(data, min_date, max_date)
        return data

    class ResizeCommand:
        def __init__(self, controller, size):
            self.controller = controller
            self.size = size
        def __call__(self):
            self.controller.set_size(self.size)

    class LoadDataCommand:
        def __init__(self, frame, data_name):
            self.frame = frame
            self.data_name = data_name
        def __call__(self):
            df = self.frame.load_data(self.data_name)
            self.frame.plot_data(df, self.data_name)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')

        label = tk.Label(self, text='"Online" Weather', bg='white', font=BIG_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=10)

        label = tk.Label(self, text='Group 12', bg='white', font=MEDIUM_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=(2, 100))

        for name in ('Emil Karlström', 'Alexander Svensson', 'Dennis Kyrk', 'Adam Alrefai', 'Modde'):
            label = tk.Label(self, text=name, bg='white', font=SMALL_FONT)
            label.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        btn = tk.Button(self, text='Next', bg='white', font=MEDIUM_FONT, command=lambda: controller.set_frame(GraphPage))
        btn.pack(side=tk.BOTTOM, expand=False, pady=10)

START_FRAME = StartPage
PAGES = (GraphPage, StartPage)