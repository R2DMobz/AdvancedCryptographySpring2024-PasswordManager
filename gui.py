'''
a gui program using tkinter for encrypting and decrypting files selected by the user.
also serves as a basic text editor for opening, editing, and saving files.
---
created by @nicholaswile
'''

import aes_256_api as aes
import tkinter as tk
from tkinter import filedialog

# TODO: Need to add key generator to GUI
global key
key = '192837465192837465'

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    with open(file_path, mode="rb") as file:
        plain_box.delete("1.0", tk.END)
        plain_box.insert(tk.END, file.read())

def process_file(is_encrypting):
    processed_path = ""
    if not file_path:
        # text = "Please select a file to process"
        # cipher_box.delete("1.0", tk.END)
        # cipher_box.insert(tk.END, text)
        return
    elif is_encrypting:
        text = f"Encrypting {file_path}, this may take up to a minute, please wait..."
        cipher_box.delete("1.0", tk.END)
        cipher_box.insert(tk.END, text)
        processed_path = aes.encrypt(file_path, key)
    else:
        text = f"Decrypting {file_path}, this may take up to a minute, please wait..."
        cipher_box.delete("1.0", tk.END)
        cipher_box.insert(tk.END, text)
        processed_path = aes.decrypt(file_path, key) 
    if len(processed_path) > 0:  
        cipher_box.delete("1.0", tk.END)
        with open(processed_path, mode = "rb") as file:
            text = file.read()
            cipher_box.insert(tk.END, text)

def selected_mode():
    selected_mode_var = mode_var.get()
    process_button.config(text=selected_mode_var.capitalize(), command=lambda: process_file(is_encrypting=(selected_mode_var == "encrypt")))
    # send_button.config(state=(tk.ACTIVE if selected_mode_var == "encrypt" and plain_box.get("1.0", tk.END) else tk.DISABLED))

window = tk.Tk()
window.title("File Encryptor")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

# Side by side text boxes
plain_box = tk.Text(window)
cipher_box = tk.Text(window)
plain_box.pack(side=tk.TOP)
cipher_box.pack(side=tk.BOTTOM)

mode_var = tk.StringVar(value="encrypt")
global selected_mode_var
selected_mode_var = mode_var
encrypt_button = tk.Radiobutton(window, text="Encrypt", variable=mode_var, value="encrypt", command=selected_mode)
decrypt_button = tk.Radiobutton(window, text="Decrypt", variable=mode_var, value="decrypt", command=selected_mode)
encrypt_button.pack(side=tk.LEFT)
decrypt_button.pack(side=tk.LEFT)

open_button = tk.Button(window, text="Open File", command=open_file)
process_button = tk.Button(window, text="Encrypt", command=lambda: process_file(is_encrypting=True))
# Get this damn thing working
send_button = tk.Button(window, text="Send File", state=tk.DISABLED)

send_button.pack(side=tk.RIGHT)
process_button.pack(side=tk.RIGHT)
open_button.pack(side=tk.RIGHT)

window.mainloop()