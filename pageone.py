import datetime
import json
import re
import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import pandas as pd

from config import REG_FONT, green, grey, database, views, grey2, show, hide, excel, chart
from gridresult import GridResult


# Page One (Quick Search Page)
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # define vars
        self.view = None
        self.date = None
        self.names = None
        self.data = None
        self.srch = None
        self.fname = None
        self.label2 = None
        # db connection
        print(database)
        self.conn = sqlite3.connect(database)
        self.cur = None

        # get view names
        with open(views) as json_file:
            self.views = sorted(json.load(json_file))

        # add entry bar in labelframe
        self.entry = tk.LabelFrame(self, text='Enter comma separated RSSD Ids', font=REG_FONT, fg='white')
        self.e = tk.Entry(self.entry)
        # search button triggers callback
        search_button = ttk.Button(self.entry, text="Search", style='my.TButton', command=self.callback)
        self.e.pack(fill='x', pady=10, padx=10)
        search_button.pack()
        # date selector treeview in LabelFrame widget
        self.leftframe = tk.Frame(self, bg=green)
        self.dateselector = tk.LabelFrame(self.leftframe, text='Date Selection', width=150, height=275, font=REG_FONT, fg='white')
        self.dateselector.tv = ttk.Treeview(self.dateselector, columns='Dates', show='headings', height=14)
        self.dateselector.tv.heading(0, text="Dates")
        self.dateselector.tv.pack()
        self.dateselector.pack(side='top')
        self.viewselector = tk.LabelFrame(self.leftframe, text='View Selection', width=150, height=275, font=REG_FONT, fg='white')
        self.viewselector.tv = ttk.Treeview(self.viewselector, columns='Views', show='headings', height=14)
        self.viewselector.tv.heading(0, text="Views")
        self.viewselector.tv.pack()
        self.viewselector.pack(side='top')
        # canvas will contain GridResults object bound to date and view selector
        self.res = tk.LabelFrame(self, text='Search Results', width=850, height=550, font=REG_FONT, fg='white')
        self.results = tk.Frame(self.res, bg='gray')
        self.results.pack_propagate(False)
        # initialize data table with parent self.results
        self.results.tvr = GridResult(self.results)
        spc = tk.Frame(self.results, width='3', bg='gray')
        spc.grid(row=0, column=1, sticky='ns')

        self.resultsMenu = tk.Frame(self.results, width=40, bg=grey2)

        self.showicon = tk.PhotoImage(file=show)
        self.hideicon = tk.PhotoImage(file=hide)
        self.excelicon = tk.PhotoImage(file=excel)
        self.charticon = tk.PhotoImage(file=chart)

        self.showHide = tk.Button(self.resultsMenu, image=self.hideicon, width=40, height=30, command=self.toggleHide)
        self.showHide.image = self.hideicon
        self.showHide.var = tk.IntVar()
        self.showHide.var.set(0)
        self.showHide.pack(side='top', pady=2)
        self.excl = tk.Button(self.resultsMenu, image=self.excelicon, width=40, height=30, command=self.popup)
        self.excl.image = self.excelicon
        self.excl.pack(side='top', pady=2)
        self.chart = tk.Button(self.resultsMenu, image=self.charticon, width=40, height=30, command=None)
        self.chart.image = self.charticon
        self.chart.pack(side='top', pady=2)
        self.resultsMenu.grid(row=0, column=4, sticky='ns')

        # pack widgets to PageOne Frame
        self.entry.grid(row=2, column=0, columnspan=2, padx=10, sticky='we')
        self.leftframe.grid(row=3, column=0, rowspan=2, sticky='ns', padx=10, pady=10)
        self.res.grid(row=3, column=1, rowspan=3, pady=10, padx=10, sticky='nsew')
        self.results.grid(row=0, column=0, sticky='nsew')
        self.results.grid_columnconfigure(2, weight=1)
        self.results.grid_columnconfigure(0, weight=1)
        self.results.grid_rowconfigure(0, weight=1)
        self.res.grid_columnconfigure(0, weight=1)
        self.res.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.configure(bg=green)
        self.entry.configure(bg=green)
        self.dateselector.configure(bg=green)
        self.viewselector.configure(bg=green)
        self.res.configure(bg=green)

    def callback(self):
        # format raw string
        self.srch = tuple(re.split(',', self.e.get()))

        # get dates and sort
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT DISTINCT repdte FROM dates')
        dates = [x[0] for x in self.cur.fetchall()]
        self.cur.close()
        dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))

        # add dates to dateselector treeview
        self.dateselector.tv.heading(0, text="Dates")
        self.dateselector.tv.bind('<<TreeviewSelect>>', self.callback2)
        for x in dates:
            self.dateselector.tv.insert('', 'end', values=x)
        self.dateselector.tv.pack()

        # add views to viewselector treeview
        self.viewselector.tv.heading(0, text="Views")
        self.viewselector.tv.bind('<<TreeviewSelect>>', self.callback2)
        for x in self.views:
            self.viewselector.tv.insert('', 'end', values=x)
        self.viewselector.tv.pack()
        self.conn.close()

    # handle changing date & view selection
    def callback2(self, event):
        # get active date & view selection
        self.date = tuple([self.dateselector.tv.item(x)['values'][0] for x in self.dateselector.tv.selection()])
        self.view = tuple([self.viewselector.tv.item(x)['values'][0] for x in self.viewselector.tv.selection()])

        # query database with selection
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        query = []

        sql = []
        if (len(self.date) > 0 and len(self.view) > 0):
            dates = sorted(self.date, key=lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))
            query = []

            for x in self.srch:
                sql = "SELECT * FROM " + str(self.view[0]) + " WHERE repdte IN ("

                for iy, y in enumerate(dates, 1):

                    if iy == len(dates):
                        sql += ("'"+y+"') AND fed_rssd='"+str(x)+"';")

                    else:
                        sql += ("'"+y+"',")

                query.append(sql)
            # format into chartresult
            self.data = []
            for x in query:
                self.cur.execute(x)
                q = self.cur.fetchall()
                self.names = [x[0] for x in self.cur.description]
                s = None
                for y in q:
                    if s is None:
                        df = dict(zip(self.names, y))
                        s = pd.DataFrame(df, index=df.keys(), columns=[df['repdte']])
                        df = pd.Series(df, index=df.keys())
                        s[df['repdte']] = df
                    else:
                        df = dict(zip(self.names, y))
                        df = pd.Series(df, index=df.keys())
                        s[df['repdte']] = df
                s = s[dates]
                self.data.append(s)
            self.results.tvr.build(srch=self.srch, date=self.date, data=self.data, names=self.names)
        self.conn.close()

        # clear charts
        for k, v in self.results.tvr.cr.w_list.items():
            try:
                for x in v:
                    x.destroy()
            except Exception:
                pass

    def toggleHide(self):
        x = self.showHide.var.get()
        if x == 0:
            self.entry.grid_remove()
            self.leftframe.grid_remove()
            self.showHide.config(image=self.showicon)
            self.showHide.image = self.showicon
            return self.showHide.var.set(1)
        else:
            self.entry.grid()
            self.leftframe.grid()
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
        if self.data is not None:
            if self.fname is not None:
                filepath = self.fname + '/quickSearchResults.xlsx'
                writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
                for x in range(len(self.data)):
                    self.data[x].to_excel(writer, sheet_name=self.srch[x])
                writer.save()

