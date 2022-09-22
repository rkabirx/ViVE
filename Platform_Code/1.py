#! /usr/bin/env python3
import tkinter as tk

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky='new')
mainframe.grid_columnconfigure(0, weight=3)

frame1 = tk.Frame(mainframe)
frame1.grid(column=0, row=0, sticky='new')
for i in range(1,4):
    frame1.grid_columnconfigure(i, weight=3, uniform='columns')



for i in range(1, 4):
    header = tk.Label(frame1, text=f'Header {i}')
    header['relief'] = 'solid'
    header['borderwidth'] = 1
    header['highlightthickness'] = 1
    header['highlightbackground'] = 'grey65'
    header.grid(column=i, row=0, sticky='ew')

frame2 = tk.Frame(mainframe)
frame2.grid(column=0, row=1, sticky='new')
for i in range(1, 4):
    frame2.columnconfigure(i, weight=3, uniform='table')

table_data = ['This is some data for row 1', 'Data for row 2', 'Data for row 3. This could be anything']

column = 1
for tdata in table_data:
    data = tk.Label(frame2, text=tdata)
    data['relief'] = 'solid'
    data['borderwidth'] = 1
    data['highlightthickness'] = 1
    data['highlightbackground'] = 'grey65'
    data.grid(column=column, row=0, sticky='ew')
    column += 1

root.mainloop()