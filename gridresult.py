import tkinter as tk
from tkinter import ttk

from chartresult import ChartResult
from config import grey


# GridResult Frame contains tables, child of Pageone.results
class GridResult(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.frame = tk.Frame(self)

        self.frame.configure(bg='orange')
        self.configure(bg=grey)
        self.create_window(0, 0, anchor='nw', window=self.frame)
        self.parent = parent
        #self.config(width=425, height=590)
        self.tv_list = []
        self.cr_list = []
        self.date = []
        self.width = None
        self.data = []
        self.sb = tk.Scrollbar(self.parent, orient='horizontal')
        self.sb.grid(row=2, column=0,sticky='sew')
        self.sb2 = tk.Scrollbar(self.parent, orient='horizontal')
        self.sb2.grid(row=2, column=2, sticky='sew')
        self.sby = tk.Scrollbar(self.parent)
        self.sby.grid(row=0, column=3, rowspan=3, sticky='ns')
        self.grid(row=0, column=0, sticky='nsew')
        self.cr = ChartResult(self.parent)
        self.sb2.config(command=self.cr.xview)


        def scroll_y(*args):
            self.yview(*args)
            self.cr.yview(*args)

        self.sb.config(command=self.xview)

        self.sby.config(command=scroll_y)

        self.config(xscrollcommand=self.sb.set)
        self.config(yscrollcommand=self.sby.set)
        self.config(bd=0, highlightthickness=0)

        self.cr.config(yscrollcommand=self.sby.set)
        self.cr.config(xscrollcommand=self.sb2.set)

    # build updates with current selection
    def build(self, **kwargs):

        #self.config(bd=0, highlightthickness=0)
        srch = kwargs['srch']
        date = kwargs['date']
        self.date = date
        self.data = kwargs['data']
        names = kwargs['names']
        # create TreeViews
        for x in self.tv_list:
            x.destroy()
        self.tv_list = []
        for x in range(len(self.data)):
            tvx = ttk.Treeview(self.frame, columns=self.data[x].columns.tolist(), show='tree headings', height=15)
            # cr = ChartResult(self.frame2, df=None)
            tvx.heading('#0', text=srch[x])
            tvx.column('#0', stretch=True, width=85)
            if len(date) >= 1:
                for y in range(len(date)):
                    ix = '#' + str(y+1)
                    tvx.heading(ix, text=date[y])
                    tvx.column(ix, stretch=True, width='80')
                for z in range(len(names)):
                    tvx.insert('', z+1, text=str(names[z]), values=self.data[x].loc[names[z]].values.tolist(), tag=x)

                tvx.grid(row=x, column=0, pady=1.5)
                self.tv_list.append(tvx)
                # bind GridResult.TreeViews to ChartResult
                tvx.bind("<<TreeviewSelect>>", self.callback)
            tvx.update()
        self.grid(row=0, column=0, sticky='nsew')
        #self.grid_rowconfigure(0, weight=1)
        self.update_idletasks()
        self.config(scrollregion=self.frame.bbox('all'))


    # destroy the widget, unused
    def clear(self):
        try:
            self.destroy()
        except Exception:
            print('error')
            pass

    # handle callback for Charts
    def callback(self, event):
        ew = event.widget
        row = ew.grid_info()['row']
        self.cr.build(ew, self.date, self.data)
        self.update_idletasks()

        self.cr.update_idletasks()
        crh = self.frame.winfo_height()
        crw = self.cr.frame.winfo_width()
        self.cr.config(scrollregion=(0,0,crw,crh))
        self.configure(bg=grey)