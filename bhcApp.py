import tkinter as tk
from tkinter import ttk

from aggstats import AggStats
from config import REG_FONT, REG_BOLD, green
from customsearch import CustomSearch
from customview import CustomViews
from importdata import ImportData
from pageone import PageOne


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "BHC Database App")

        # container holds active page
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=None)
        menubar.add_cascade(label="File", menu=filemenu)

        # navigation buttons
        navbar = tk.Frame(container)

        style = ttk.Style()
        style.configure('my.TButton', font=REG_FONT, background=green)
        # objects
        navlbl = tk.Label(navbar, text='Navigation Menu: ', font=REG_BOLD, fg='white', bg=green)
        homebtn = ttk.Button(navbar, text='Quick Search', style='my.TButton',
                             command=lambda: self.show_frame(PageOne))
        customsrchbtn = ttk.Button(navbar, text='Custom Search', style='my.TButton',
                                   command=lambda: self.show_frame(CustomSearch))
        importdata = ttk.Button(navbar, text='Import Data', style='my.TButton',
                                command=lambda: self.show_frame(ImportData))
        aggstats = ttk.Button(navbar, text='User Guide', style='my.TButton',
                                command=lambda: self.show_frame(AggStats))
        calcfields = ttk.Button(navbar, text='Manage Config', style='my.TButton',
                                command=lambda: self.show_frame(CustomViews))

        navlbl.pack(side='left', pady=10, padx=10)
        homebtn.pack(side='left', pady=10)
        customsrchbtn.pack(side='left', pady=10)
        importdata.pack(side='left', pady=10)
        calcfields.pack(side='left', pady=10)
        aggstats.pack(side='left', pady=10)
        navbar.configure(bd=1, relief='raised')
        navbar.configure(bg=green)

        tk.Tk.config(self, menu=menubar)
        navbar.grid(row=0, sticky='ew')
        print('navbar')
        self.frames = {}
        # page navigation
        for F in (PageOne, CustomSearch, CustomViews, AggStats, ImportData):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=1, column=0, sticky='nsew')
        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# 746223,3317192,564856,419255,350657,148470,3048487
# run the app
if __name__ == "__main__":
    print('[746223,3317192,564856,419255,350657,148470,3048487]')
    app = MainApp()
    app.mainloop()
