import tkinter

import finviz
import json
import os
from tkinter import *
from tkinter import ttk
from pathlib import Path
import copy


def reload_data_file():
    sc = finviz.Screener()  # to write data from internet into the file
    data = sc.data

    with open("finviz_data.txt", "w") as fv:
        for i in data:
            if i['P/E'] == '-':
                i['P/E'] = '0'
            if i['Market Cap'] == '-':
                i['Market Cap'] = '0M'
            json.dump(i, fv)
            fv.write("\n")


def reload_update(Frame: Tk):
    reload_data_file()
    Frame.update()


class Table(tkinter.Frame):
    game_frame = None
    CONST_LS = None
    stock_ls = []
    game_scroll = None
    game_scroll_1 = None
    my_game = None
    d_B_M = {"B": 1, "M": 1000}# dict for billions or millions

    def __init__(self, _stock_ls, ws):
        self.root = ws
        self.CONST_LS = copy.deepcopy(_stock_ls)
        self.stock_ls = _stock_ls
        super().__init__(ws)
        self.game_frame = Frame(ws)

        self.game_frame.pack()

        # scrollbar
        self.game_scroll = Scrollbar(self.game_frame)
        self.game_scroll.pack(side=RIGHT, fill=Y)

        self.game_scroll_1 = Scrollbar(self.game_frame, orient='horizontal')
        self.game_scroll_1.pack(side=BOTTOM, fill=X)

        self.my_game = ttk.Treeview(self.game_frame, yscrollcommand=self.game_scroll.set,
                                    xscrollcommand=self.game_scroll_1.set)

        self.my_game.pack()

        self.game_scroll.config(command=self.my_game.yview)
        self.game_scroll_1.config(command=self.my_game.xview)
        # define our column

        self.my_game['columns'] = tuple(self.stock_ls[0].keys())

        # format our column
        self.my_game.column("#0", width=0, stretch=NO)
        self.my_game.column(tuple(self.stock_ls[0].keys())[0], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[1], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[2], anchor=CENTER, width=200)
        self.my_game.column(tuple(self.stock_ls[0].keys())[3], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[4], anchor=CENTER, width=120)
        self.my_game.column(tuple(self.stock_ls[0].keys())[5], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[6], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[7], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[8], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[9], anchor=CENTER, width=100)
        self.my_game.column(tuple(self.stock_ls[0].keys())[10], anchor=CENTER, width=100)

        # Create Headings
        self.my_game.heading("#0", text="", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[0], text="No.", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[1], text="Ticker", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[2], text="Company", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[3], text="Sector", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[4], text="Industry", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[5], text="Country", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[6], text="Market Cap", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[7], text="P/E", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[8], text="Price", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[9], text="Change", anchor=CENTER)
        self.my_game.heading(tuple(self.stock_ls[0].keys())[10], text="Volume", anchor=CENTER)

        # add data

        self.reload_table(self.stock_ls)

        # reload file button
        btn_reload = Button(text="Reload File", pady="500", height=10, width=20, command=lambda: [reload_update(ws)])
        btn_reload.pack(side=tkinter.LEFT)
        # sort by country

        self.message = StringVar()
        Country_entry = Entry(textvariable=self.message)
        Country_entry.place(relx=.3, rely=0.95, anchor="c")

        Country_button = Button(text="Sort by country",
                                command=lambda: [self.sort_country()])
        Country_button.place(relx=.3, rely=.85, anchor="c")

        Sort_value_button = Button(text="Sort by stock price",
                                   command=lambda: [self.sort_stock_price()])
        Sort_value_button.place(relx=.4, rely=.85, anchor="c")
        Sort_PE_button = Button(text="Sort by P/E",
                                command=lambda: [self.sort_PE()])
        Sort_PE_button.place(relx=.5, rely=.85, anchor="c")
        Sort_MC_button = Button(text="Sort by Market Cap",
                                command=lambda: [self.sort_Market_Cap()])
        Sort_MC_button.place(relx=.6, rely=.85, anchor="c")

    def reload_table(self, _ls: list):
        for i in self.my_game.get_children():
            self.my_game.delete(i)
        for i in range(len(_ls)):
            self.my_game.insert(parent='', index='end', iid=i, text='', values=list(_ls[i].values()))

    def sort_PE(self):
        tmp = sorted(self.stock_ls, key=lambda x: float(x['P/E']), reverse=True)

        if dict_of_list_comparion(tmp, self.stock_ls):
            self.stock_ls = sorted(self.stock_ls, key=lambda x: float(x['P/E']), reverse=False)
        else:
            self.stock_ls = sorted(self.stock_ls, key=lambda x: float(x['P/E']), reverse=True)
        self.reload_table(self.stock_ls)

    def sort_Market_Cap(self):
        # print(float(self.stock_ls[0]['Market Cap'][0:len(self.stock_ls[0]['Market Cap']) - 1]))
        tmp = sorted(self.stock_ls,
                     key=lambda x: float(x['Market Cap'][0:len(x['Market Cap']) - 1]) / self.d_B_M[x['Market Cap'][-1]],
                     reverse=True)

        if dict_of_list_comparion(tmp, self.stock_ls):
            # print(self.stock_ls[0]['Market Cap'][0:len(self.stock_ls[0]['Market Cap']) - 1])
            self.stock_ls = sorted(self.stock_ls,
                                   key=lambda x: float(x['Market Cap'][0:len(x['Market Cap']) - 1]) / self.d_B_M[
                                       x['Market Cap'][-1]], reverse=False)
        else:
            self.stock_ls = sorted(self.stock_ls,
                                   key=lambda x: float(x['Market Cap'][0:len(x['Market Cap']) - 1]) / self.d_B_M[
                                       x['Market Cap'][-1]], reverse=True)
        self.reload_table(self.stock_ls)

    def sort_country(self):
        tmp = []
        if self.message.get() == '':

            tmp = self.CONST_LS

        else:
            for i in self.stock_ls:
                if i['Country'] == self.message.get():
                    tmp.append(i)

        self.reload_table(tmp)
        # self.update()

    def sort_stock_price(self):
        tmp = sorted(self.stock_ls, key=lambda x: float(x['Price']), reverse=True)
        if dict_of_list_comparion(tmp, self.stock_ls):
            self.stock_ls = sorted(self.stock_ls, key=lambda x: float(x['Price']), reverse=False)
        else:
            self.stock_ls = sorted(self.stock_ls, key=lambda x: float(x['Price']), reverse=True)
        self.reload_table(self.stock_ls)


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def dict_of_list_comparion(first_list: list, second_list: list):
    if len(first_list) != len(second_list):
        return False
    for k, v in zip(first_list, second_list):
        if k != v:
            return False
    return True


def main():
    ls = []

    ws = Tk()
    ws.title('Stock program')
    ws.geometry('1000x500')
    ws['bg'] = '#AC99F2'

    fv_file_path = Path("finviz_data.txt")
    if fv_file_path.stat().st_size == 0:
        reload_data_file()

    with open("finviz_data.txt", "r") as fv:
        for i in fv:
            ls.append(json.loads(i))

    table = Table(ls, ws)
    table.pack(expand=tkinter.YES, fill=tkinter.BOTH)
    ws.mainloop()
    # print(len(ls))
    # print(ls)
    # for i in ls:
    #     print(i, "\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
