import csv
import json
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import pandas as pd

from config import REG_BOLD, green, grey, database, dupku, comm, exclude


class ImportData(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        with open(comm) as json_file:
            self.common = json.load(json_file)
        with open(dupku) as json_file:
            self.dupku = json.load(json_file)
        with open(exclude) as json_file:
            self.exclude = json.load(json_file)
        df = pd.Series(self.dupku)
        mask = self.exclude + self.common
        self.mask = list(df[~df.isin(mask)])
        self.mainlist = None
        self.lbl = tk.LabelFrame(self, text='Choose a folder to upload', font=REG_BOLD, fg='black')
        self.lbl.configure(bg=grey, height=200)
        button = ttk.Button(self.lbl,text='Browse Folders', command=lambda: self.openFolder())
        button.pack(side='top', padx=10, pady=10)
        frame = tk.Frame(self.lbl)
        label2 = tk.Label(frame, text='Selected folder path: ', bg=grey, font=REG_BOLD, fg='black')
        self.label1 = tk.Label(frame, text='results appear here',font=REG_BOLD, fg='grey', bg=grey)
        self.lbl.pack( anchor='n', padx=10, pady=10, expand=True)
        label2.pack(side='left')
        self.label1.pack(side='left')
        frame.pack(side='top')
        self.btn = ttk.Button(self.lbl, text='Add to database', command=lambda: self.uploadData())
        self.fname = None

        self.configure(bg=green)

    def openFolder(self):
        self.fname = filedialog.askdirectory()
        if self.fname:
            self.label1.configure(text=self.fname)
            self.btn.pack(side='top', padx=10, pady=10)

    def uploadData(self):

        def insert_stmnt_bnks(common):
            st = 'INSERT OR REPLACE INTO banks('
            common = pd.Series(common)
            exclude = ['inst.webaddr', 'fed_rssd', 'rssd_date', 'repdte', 'webaddr', 'edepfor', 'idFRANUM', 'ifiduc',
                       'ilnfor', 'ntrcdsm', \
                       'trexer', 'tract', 'trpower']
            common = common[~common.isin(exclude)]
            key = ['fed_rssd'] + list(common)
            valstrng = 'VALUES('
            for ix, x in enumerate(key):
                if ix == (len(key) - 1):
                    st += x + ') '
                    valstrng += '?);'
                else:
                    st += x + ', '
                    valstrng += '?, '
            sql = st + valstrng
            return sql

        def create_task_banks(mainlist, common, conn):
            sql = insert_stmnt_bnks(common)
            c = conn.cursor()
            exclude = ['inst.webaddr', 'fed_rssd', 'rssd_date', 'repdte', 'webaddr', 'edepfor', 'idFRANUM', 'ifiduc',
                       'ilnfor', 'ntrcdsm',
                       'trexer', 'tract', 'trpower']
            common = pd.Series(common)
            common = common[~common.isin(exclude)]
            common = list(common)
            for x in range(len(mainlist)):
                if x % 1000 == 0:
                    conn.commit()

                df = pd.Series(mainlist[x])
                key = ['fed_rssd'] + common
                df = df[key]
                if len(df) != 36:
                    print((x, len(df)))
                task = ()
                for k, v in df.items():
                    task += (str(v),)
                c.execute(sql, task)
            conn.commit()
            return c.close()

        def insert_data(mainlist,subset,conn):
            c = conn.cursor()
            sql1 = 'INSERT OR REPLACE INTO data ('
            sql2 = 'UPDATE data SET '
            s1 = ['rssd_date', 'fed_rssd', 'repdte']
            s1 += subset[:500]
            s2 = subset[500:]
            df1 = pd.Series
            for ix, x in enumerate(s1, 1):
                if ix == len(s1):
                    sql1 += (x + ') VALUES (') + ('?,' * (ix-1)) + '?);'
                else:
                    sql1 += x + ','

            for ix, x in enumerate(s2, 1):
                if ix == len(s2):
                    sql2 += x + '=? WHERE rssd_date='
                else:
                    sql2 += x + '=?,'

            for ix, x in enumerate(mainlist):
                if ix % 100 == 0:
                    print(ix)
                task1 = ()
                task2 = ()
                rssdDate = x['rssd_date']
                sql2x = sql2 + ('"{}";'.format(str(rssdDate)))
                df1 = pd.Series(x)[s1]
                df2 = pd.Series(x)[s2]
                for k, v in df1.items():
                    if k in ['rssd_date', 'fed_rssd', 'repdte']:
                        val = (str(v),)
                    else:
                        try:
                            val = (float(v),)
                        except ValueError:
                            val = (0,)
                    task1 += val
                for k, v in df2.items():
                    try:
                        val = (float(v),)
                    except ValueError:
                        val = (0,)
                    task2 += val
                c.execute(sql1,task1)
                c.execute(sql2x, task2)
                conn.commit()






        def create_task_dates(mainlist,conn):
            task = (mainlist[0]['repdte'],)
            sql = 'INSERT OR REPLACE INTO dates(repdte) VALUES(?)'
            c = conn.cursor()
            c.execute(sql,task)
            conn.commit()
            return c.close()

        root = self.fname
        maindict = {}
        print('maindict init')
        for file in os.listdir(root):
            if file.endswith('.csv'):
                filepath = root + '/' + file
                with open(filepath, encoding="ISO-8859-1") as csvfile:
                    data = csv.DictReader(csvfile)
                    for row in data:
                        row['rssd_date'] = row['fed_rssd'] + row['repdte']
                        if row['rssd_date'] in maindict.keys():
                            for k, v in row.items():
                                maindict[row['rssd_date']].update({k: v})
                        else:
                            new = {k: v for k, v in row.items()}
                            maindict.update({row['rssd_date']: new})
        self.mainlist = [v for k,v in maindict.items()]
        for x in self.mainlist:
            for z in self.dupku:
                if z not in x.keys():
                    x.update({z: '0'})

        conn = sqlite3.connect(database)
        with conn:
            print('BEGIN UPLOAD')
            create_task_banks(self.mainlist, self.common, conn)
            print('BANKS COMPLETE')
            create_task_dates(self.mainlist, conn)
            print('DATES COMPLETE')
            insert_data(self.mainlist, self.mask, conn)
            print('DATA COMPLETE')
            conn.commit()
        conn.close()
        print('done')
