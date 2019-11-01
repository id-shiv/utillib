import tkinter as tk
from tkinter import filedialog, Text
import os

app = tk.Tk()


def add_file():
    file_name = filedialog.askopenfile(initialdir="/", title="Select Directory")
    print(file_name)


canvas = tk.Canvas(app, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(app, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

open_file = tk.Button(frame, text="Open File", padx=10, pady=5, fg="black", bg="orange", command=add_file)
open_file.pack()

run_apps = tk.Button(frame, text="Run Apps", padx=10, pady=5, fg="black", bg="orange")
run_apps.pack()

app.mainloop()