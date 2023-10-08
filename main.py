import os
import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import *


def select_directory():
    directory = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, directory)
    adjust_entry_width(directory)


def search():
    print('hello')
    directory = source_entry.get()
    hashes = {}
    dups = []
    check_type = []
    images = ['JPG', 'JPEG', 'PNG', 'GIF', 'WEBP', 'TIFF', 'PSD', 'RAW', 'BMP', 'INDD', 'SVG', 'AI', 'EPS', 'PDF']
    docs = ['doc', 'docx', 'html', 'htm', 'odt', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'txt', 'key']
    videos = ['mp4', 'avi', 'mov', 'flv', 'acvhd']
    audio = ['mp3', 'pcm', 'wav', 'aiff', 'aac', 'ogg', 'wma', 'flac', 'alac', 'wma']
    if CheckVar1.get() == 1:
        check_type = check_type + images
    elif CheckVar2.get() == 1:
        check_type = check_type + docs
    elif CheckVar3.get() == 1:
        check_type = check_type + videos
    elif CheckVar4.get() == 1:
        check_type = check_type + audio

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if check_type is []:
                file_hash = hash_file(filepath)
                if file_hash in hashes:
                    dups.append(filepath)
                else:
                    hashes[file_hash] = filepath
            else:
                for file_type in check_type:
                    if filepath.endswith(file_type):
                        file_hash = hash_file(filepath)
                        if file_hash in hashes:
                            dups.append(filepath)
                        else:
                            hashes[file_hash] = filepath
    print(dups)
    return dups


def hash_file(path, block_size=65536):
    hasher = hashlib.md5()
    with open(path, 'rb') as file:
        data = file.read(block_size)
        while data:
            hasher.update(data)
            data = file.read(block_size)
    return hasher.hexdigest()


def adjust_entry_width(text):
    source_entry.config(width=len(text) + 3)

def reset(flag=False):
    if flag:
        if CheckVar5.get():
            print("reset 1-4")
            CheckVar1.set(0)
            CheckVar2.set(0)
            CheckVar3.set(0)
            CheckVar4.set(0)
        elif CheckVar1.get() or CheckVar2.get() or CheckVar3.get() or CheckVar4.get():
            print("reset 5")
            CheckVar5.set(0)
    else:
        if CheckVar5.get():
            CheckVar5.set(0)


# Create the main window
window = tk.Tk()
window.title("No More Duplicates")
source_label = tk.Label(window, text="Source Directory:")
source_label.grid(row=0, column=0, sticky="w")
source_entry = tk.Entry(window)
source_entry.grid(row=0, column=1)
source_entry.grid(columnspan=2, padx=10)
browse_button = tk.Button(window, text="Browse", command=select_directory)
browse_button.grid(row=0, column=3)
browse_button.grid(padx=10)
file_type_label = tk.Label(window, text="File Type:")
file_type_label.grid(row=2, column=0, sticky="w")
CheckVar1 = tk.IntVar()
CheckVar2 = tk.IntVar()
CheckVar3 = tk.IntVar()
CheckVar4 = tk.IntVar()
CheckVar5 = tk.IntVar()
C1 = Checkbutton(window, text="Images", variable=CheckVar1, onvalue=1, offvalue=0, command=lambda: reset(True))
C2 = Checkbutton(window, text="Documents", variable=CheckVar2, onvalue=1, offvalue=0, command=lambda: reset(True))
C3 = Checkbutton(window, text="Audio", variable=CheckVar3, onvalue=1, offvalue=0, command=lambda: reset(True))
C4 = Checkbutton(window, text="Videos", variable=CheckVar4, onvalue=1, offvalue=0, command=lambda: reset(True))
C5 = Checkbutton(window, text="All", variable=CheckVar5, onvalue=1, offvalue=0, command=lambda: reset(True))
CheckVar5.set(1)
C1.grid(row=3, column=0, sticky="w")
C2.grid(row=4, column=0, sticky="w")
C3.grid(row=5, column=0, sticky="w")
C4.grid(row=6, column=0, sticky="w")
C5.grid(row=7, column=0, sticky="w")
search_button = tk.Button(window, text="Find Duplicates!", command=search)
search_button.grid(row=8, column=0, sticky="w", padx=5)
result_label = tk.Label(window, text="", fg="green")
result_label.grid(row=9, column=0, columnspan=2, pady=10)

window.mainloop()
