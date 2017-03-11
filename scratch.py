import tkinter as tk
from tkinter import ttk
import pyperclip
import time

root = tk.Tk()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(root)
listbox.pack()


listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

recent_value = ''
def get_input():
    global recent_value
    # while abs(time.time() - start) < 10:
    new_value = pyperclip.paste()
    if new_value != recent_value:
        recent_value = new_value
        listbox.insert(tk.END, new_value)
    root.after(100, get_input)

def get_item(evt):
    value = listbox.get(listbox.curselection())
    pyperclip.copy(value)

listbox.bind('<<ListboxSelect>>', get_item)

butt = tk.Button(root, text='Delete All', command=lambda lb=listbox: lb.delete(0, tk.END))
butt.pack()

root.after(100, get_input)

root.mainloop()
