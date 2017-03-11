import tkinter as tk
import pyperclip
from tkinter import font


root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(frame, font= font.Font(size=12))
# listbox.grid(row=0, column=0, columnspan=5, rowspan=10)
listbox.pack(side='left')

scrollbar = tk.Scrollbar(frame, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

recent_value = ''
def get_input():
    global recent_value
    new_value = pyperclip.paste()
    if new_value != recent_value:
        recent_value = new_value
        listbox.insert(0, new_value)
    root.after(100, get_input)

def get_item(evt):
    value = listbox.get(listbox.curselection())
    pyperclip.copy(value)

listbox.bind('<<ListboxSelect>>', get_item)

clear_button = tk.Button(root, text='Clear list', command=lambda lb=listbox: lb.delete(0, tk.END), width=10)
# clear_button.grid(row=0, column=6)
clear_button.pack(anchor='e')

def close_window():
    root.destroy()

exit_button = tk.Button(root, text='Exit', command=close_window, width=10)
# exit_button.grid(row=1, column=6)
exit_button.pack(anchor='e')


root.after(100, get_input)

root.mainloop()
