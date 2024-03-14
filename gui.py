'''
a gui program using tkinter for encrypting and decrypting files selected by the user.
also serves as a basic text editor for opening, editing, and saving files.
---
created by @nicholaswile
'''

import aes_256_api
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

file = ""

"""Encrypt the current file."""
def encrypt_file():
    # TODO: Currently the user must select an existing file. Would like to make it work with text in the editor window
    print(file)
    if file == "":
        txt_edit.delete("1.0", tk.END)
        txt_edit.insert(tk.END, "Must select a source file to encrypt")
    else:
        # TODO: Need to add key generator to GUI
        key = '192837465192837465'  
        msg = aes_256_api.encrypt(file, key)
        txt_edit.delete("1.0", tk.END)
        txt_edit.insert(tk.END, msg)

"""Decrypt the current file."""
def decrypt_file():
    if file == "":
        txt_edit.delete("1.0", tk.END)
        txt_edit.insert(tk.END, "Must select a source file to decrypt")
    else:
        # TODO: Need to add key generator to GUI
        key = '192837465192837465'  
        msg = aes_256_api.decrypt(file, key)
        txt_edit.delete("1.0", tk.END)
        txt_edit.insert(tk.END, msg)

"""Open a file for encrypting or decrypting."""
def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="rb") as input_file:  
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"File Encryptor - {filepath}")
    # TODO: Use a better practice. LOL
    global file
    file = filepath

"""Save the current file as a new file."""
def save_file():
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"File Encryptor - {filepath}")

window = tk.Tk()
window.title("File Encryptor")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

btn_open = tk.Button(frm_buttons, text="Encrypt", command=encrypt_file)
btn_open.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

btn_open = tk.Button(frm_buttons, text="Decrypt", command=decrypt_file)
btn_open.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()