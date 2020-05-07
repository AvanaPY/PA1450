import tkinter as tk
from pages import PAGES, START_FRAME, DEFAULT_SIZE

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__('Online Weather by Group 12', *args, **kwargs)
        self.title('Online Weather by Group 12')
        self.geometry(DEFAULT_SIZE)
        self.resizable(0, 0)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self._frames = {}

        for F in PAGES:
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky='snew')
            self._frames[F] = frame
            
        self.set_frame(START_FRAME)

    def client_exit(self):
        self.quit()

    def set_size(self, size):
        self.geometry(size)
    
    def set_frame(self, f):
        frame = self._frames[f]
        frame.tkraise()

if __name__ == '__main__':
    root = Root()
    root.mainloop()