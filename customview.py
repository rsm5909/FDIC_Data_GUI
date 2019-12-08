import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from config import REG_BOLD, green, grey


class CustomViews(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.lbl = tk.LabelFrame(self, text='Custom Views Page', bg=grey, font=REG_BOLD, fg='black')
        self.fname = None
        self.label2 = tk.Label(self.lbl, text='Selected folder path: ', bg=grey, font=REG_BOLD, fg='black')
        self.label1 = tk.Label(self.lbl, text='results appear here', font=REG_BOLD, fg='grey', bg=grey)
        self.btn = ttk.Button(self.lbl, text='Load Views', command=lambda: print('button'))
        button = ttk.Button(self.lbl, text='Browse Folders', command=lambda: self.openFolder())
        self.lbl.pack(anchor='n', padx=10, pady=10)
        self.label2.pack(side='top')
        self.label1.pack(side='top')
        button.pack(side='left', padx=10, pady=10)
        self.configure(bg=green)

    def openFolder(self):
        self.fname = filedialog.askdirectory()
        if self.fname:
            self.label1.configure(text=self.fname)
            self.btn.pack(side='left', padx=10, pady=10)