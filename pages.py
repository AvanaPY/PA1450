import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import animation as animation
import matplotlib.pyplot as plt

plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y:%m:%d:%H'))
plt.gca().xaxis.set_major_locator(matplotlib.dates.HourLocator())

from matplotlib import style
style.use('ggplot')

import tkinter as tk

from tkcalendar import Calendar, DateEntry

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

        label = tk.Label(self, text='Graphing data', bg='white', font=BIG_FONT)
        label.pack()

        # Interval
        
        interval_frame = tk.Frame(self, bg='white')
        label = tk.Label(interval_frame, text='Interval', bg='white', font=MEDIUM_FONT)
        label.pack(side=tk.TOP)

        self._interval = []
        for t in ('Start', 'End'):
            time_frame = tk.Frame(interval_frame, bg='white')

            tk.Label(time_frame, text=t, bg='White', font=MEDIUM_FONT).pack(side=tk.TOP)

            entry = DateEntry(time_frame, locale='en_GB', year=2020, month=1, day=1)
            entry.pack(side=tk.LEFT, expand=True)

            variable = tk.StringVar(time_frame)
            variable.set(0)
            hour_dropdown = tk.OptionMenu(time_frame, variable, *list(range(0, 24)))
            hour_dropdown.pack(side=tk.LEFT, expand=True)

            self._interval.append((entry, variable))

            time_frame.pack(side=tk.LEFT, expand=False, padx=10)

        interval_frame.pack(side=tk.TOP, expand=False, pady=20)

        graph_frame = tk.Frame(self, bg='white')

        self._figure = Figure(figsize=(5, 5), dpi=100)
        self._plot = self._figure.add_subplot(111)
        self._plot.set_title('Graph')

        self._graph_canvas = FigureCanvasTkAgg(self._figure, graph_frame)
        self._graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def plot_data(self, dataframe, label, unit, color='red'):

        count = dataframe.shape[0]
        self._plot.clear()
        self._plot.set_title('Graph')

        # self._plot.set_xticks(dataframe['Date'])
        self._plot.set_xlabel('Date')
        self._plot.set_ylabel('Value', rotation=90)
        
        dates = [datetime.datetime.strptime(d, '%Y:%m:%d:%H') for d in dataframe['Date']]
        self._plot.plot(dates, dataframe['Value'], label=f'{label} ({unit})', color=color)
        self._plot.legend()
        plt.gcf().autofmt_xdate()

        self._graph_canvas.draw()

    def get_interval(self):
        dates = []
        for entr, hour in self._interval:
            date = entr.get_date()
            hour = hour.get()

            dt = datetime.datetime(date.year, date.month, date.day, int(hour))
            
            dates.append(dt)
        return dates

    def load_data(self, data_name):
        min_date, max_date = self.get_interval()
        if min_date.timestamp() < max_date.timestamp():
            data, unit = data_manager.load_data(data_name)
            data = data_manager.get_interval(data, min_date, max_date)
            return data, unit
        else:
            return None, None
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
            df, unit = self.frame.load_data(self.data_name)
            if not (df is None):
                self.frame.plot_data(df, self.data_name, unit)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')

        label = tk.Label(self, text='"Online" Weather', bg='white', font=BIG_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=10)

        label = tk.Label(self, text='Group 12', bg='white', font=MEDIUM_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=(2, 100))

        for name in ('Emil Karlström', 'Alexander Svensson', 'Dennis Kyrk', 'Adam Alrefai', 'Mahmoud Alsadi'):
            label = tk.Label(self, text=name, bg='white', font=SMALL_FONT)
            label.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        btn = tk.Button(self, text='Next', bg='white', font=MEDIUM_FONT, command=lambda: controller.set_frame(GraphPage))
        btn.pack(side=tk.BOTTOM, expand=False, pady=10)

START_FRAME = StartPage
PAGES = (GraphPage, StartPage)