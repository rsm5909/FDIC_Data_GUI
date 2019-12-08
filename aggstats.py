import tkinter as tk

from config import green


class AggStats(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl = tk.Label(self, text='Agg Stats Page')
        self.lbl.grid(row=1)
        self.grid_columnconfigure(1, weight=1)
        self.configure(bg=green)