import tkinter as tk
import pyperclip
from tkinter import font


root = tk.Tk()

# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(root, font= font.Font(size=12))
listbox.grid(row=0, column=0)
# listbox.pack()


# listbox.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=listbox.yview)

recent_value = ''
def get_input():
    global recent_value
    new_value = pyperclip.paste()
    if new_value != recent_value:
        recent_value = new_value
        listbox.insert(tk.END, new_value)
    root.after(100, get_input)

def get_item(evt):
    value = listbox.get(listbox.curselection())
    pyperclip.copy(value)

listbox.bind('<<ListboxSelect>>', get_item)

clear_button = tk.Button(root, text='Clear list', command=lambda lb=listbox: lb.delete(0, tk.END))
clear_button.grid(row=0, column=1)
# clear_button.pack()

def close_window():
    root.destroy()

exit_button = tk.Button(root, text='Exit', command=close_window)
exit_button.grid(row=1, column=1)
# exit_button.pack()


root.after(100, get_input)

root.mainloop()
