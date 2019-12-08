import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import pandas as pd
import pandastable as pt

from config import REG_FONT, green, grey, database, grey2, show, hide, excel


class CustomSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl = tk.LabelFrame(self, text='Enter SQL Query String', font=REG_FONT, fg='white', bg=green)
        self.lbl.config(height=200)
        self.lbl.grid(row=0, column=0, sticky='new')

        self.ctrlbar = tk.Frame(self, width=40, height=80, bg=grey2)
        self.ctrlbar.grid(row=1, column=0, pady=10, sticky='nw')
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.showicon = tk.PhotoImage(file=show)
        self.hideicon = tk.PhotoImage(file=hide)
        self.excelicon = tk.PhotoImage(file=excel)
        self.showHide = tk.Button(self.ctrlbar, image=self.hideicon, width=40, height=30, command=self.toggleHide)
        self.showHide.image = self.hideicon
        self.showHide.var = tk.IntVar()
        self.showHide.var.set(0)
        self.showHide.pack(side='left', pady=2)
        self.excl = tk.Button(self.ctrlbar, image=self.excelicon, width=40, height=30, command=self.popup)
        self.excl.image = self.excelicon
        self.excl.pack(side='left', pady=2)

        srchframe = tk.Frame(self.lbl, bg=green)
        srchframe.pack(fill='both', pady=10)

        self.entry = tk.Text(srchframe, height=5)
        self.entry.pack(fill='both')

        self.btn = ttk.Button(srchframe, text="Search", command=self.callback)
        self.btn.pack(side='bottom')
        self.var = tk.IntVar()
        self.var2 = tk.IntVar()
        self.showtable = tk.Checkbutton(srchframe, text='Add results in table', var=self.var, font=REG_FONT,
                                        fg='white', bg=green)
        self.tanspose = tk.Checkbutton(srchframe, text='Transpose Results', var=self.var2, font=REG_FONT,
                                        fg='white', bg=green)
        self.tanspose.pack(side='bottom')
        self.showtable.pack(side='bottom')
        self.lbl2 = tk.LabelFrame(self, text='Results Table', font=REG_FONT, fg='white', bg=green)
        self.lbl2.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.tableframe = tk.Frame(self.lbl2)
        self.tableframe.pack(fill='both', expand=True)
        self.df = None
        self.fname = None
        self.label2 = None
        self.table = pt.Table(self.tableframe, showtoolbar=True, showstatusbar=True)
        self.table.show()

        self.configure(bg=green)
        print('SELECT fed_rssd, (netinc/asset) AS ROA from data where repdte="3/31/2010"')

    def callback(self):
        conn = sqlite3.connect(database)
        sql = self.entry.get("1.0",tk.END)
        print(sql)
        self.df = self.table.model.df
        self.df = pd.read_sql_query(sql,conn)
        var = self.var.get()
        self.table.destroy()
        var2 = self.var2.get()
        if var2 == 1:
            self.df = self.df.transpose()
        if var == 1:
            self.table = pt.Table(self.tableframe, dataframe=self.df,showtoolbar=True, showstatusbar=True)
            self.table.show()
        print(self.df.head())

    def toggleHide(self):
        x = self.showHide.var.get()
        if x == 0:

            self.lbl.grid_remove()
            self.showHide.config(image=self.showicon)
            self.showHide.image = self.showicon
            return self.showHide.var.set(1)
        else:
            self.lbl.grid()
            self.showHide.image = self.hideicon
            self.showHide.config(image=self.hideicon)
            return self.showHide.var.set(0)

    def popup(self):
        popup = tk.Tk()
        popup.wm_title("Select a save location")
        popup.config(bg=grey)
        label = tk.Label(popup, text='Selected file path:')
        label.pack(side="top", fill="x", pady=10)
        self.label2 = tk.Label(popup, text='results appear here')
        self.label2.pack(side="top", fill="x", pady=10)
        b1 = ttk.Button(popup, text="Cancel", command=popup.destroy)
        b1.pack(side='left')
        b2 = ttk.Button(popup, text="Select Dir", command=self.getdir)
        b2.pack(side='left')
        b3 = ttk.Button(popup, text="Download", command=self.download_xl)
        b3.pack(side='left')
        popup.mainloop()

    def getdir(self):
        self.fname = filedialog.askdirectory()
        if self.fname:
            self.label2.configure(text=self.fname)

    def download_xl(self):
        if self.df is not None:
            if self.fname is not None:
                filepath = self.fname + '/CustomSearchResults.xlsx'
                writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
                self.df.to_excel(writer, sheet_name='Results')
                writer.save()

