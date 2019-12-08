import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import green, grey


# ChartResult Frame contains charts
class ChartResult(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent)
        self.frame = tk.Frame(self)
        self.frame.config(bg='gray')
        self.parent = parent
        self.create_window(0, 0, anchor='nw', window=self.frame)
        self.w_list = {}
        self.config(width=425, height=590)
        self.configure(bg=grey)
        self.config(bd=0, highlightthickness=0)
        self.grid(column=2, row=0, sticky='nsew')

    # build updates widget with current selection
    def build(self, ew, date, data):
        row = ew.grid_info()['row']
        sel = ew.selection()
        for k,v in self.w_list.items():
            if k == row:
                for x in v:
                    try:
                        x.destroy()
                    except Exception:
                        pass

        for x in range(len(data)):
            spacer = tk.Frame(self.frame, bg=grey)
            spacer.config(height=311, width=2)
            spacer.grid(column=0,row=x)
            if x not in self.w_list.keys():
                self.w_list.update({x: []})


        for x in range(len(sel)):
            plt.rcParams.update({'font.size': 8})
            title = ew.item(sel[x])['text']
            values = [pd.to_numeric(y) for y in ew.item(sel[x])['values']]
            data = {'Date': date, title: values}
            df = pd.DataFrame(data, columns=['Date', title])
            chg = df[title].pct_change()
            chg = chg *100
            figure = plt.Figure(figsize=(3, 2.5), dpi=120)
            ax = figure.add_subplot(111)
            #ax2 = ax.twinx()

            bar = FigureCanvasTkAgg(figure, self.frame)
            df.plot(kind='bar', legend=False, ax=ax, color=green)
            #chg.plot(kind='line', legend=False, ax=ax2, color=tan)
            """
            std = df[title].std()
            miny = round(df[title].min() - std, 2)
            if miny < 0:
                miny = 0
            maxy = round(df[title].max() + std, 2)
            ax.set_ylim(bottom=miny, top=maxy)
            """
            ax.set_title(title)
            ax.set_xticklabels(df['Date'], rotation=40)
            ax.set_facecolor(grey)
            figure.tight_layout()
            w = bar.get_tk_widget()
            w.grid(column=x+1, row=row, pady=1.5, padx=1.5)
            self.w_list[row].append(w)
        self.grid(column=2, row=0, sticky='nsew')
        self.update_idletasks()

    # destroy the widget, unused
    def clear(self):
        try:
            self.destroy()
        except Exception:
            print('error')
            pass