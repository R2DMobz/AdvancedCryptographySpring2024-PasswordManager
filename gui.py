'''
a gui program using tkinter for encrypting and decrypting files selected by the user.
also serves as a basic text editor for opening, editing, and saving files.
---
created by @nicholaswile (March 14th, 2024 3:52 AM) 
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import api_aes256 as aes
import api_sha3 as sha3

class FileEncryptorApp:
    # Initialize variables
    open_file_path = ""
    save_file_path = ""
    password = ""
    key = ""

    # Constructor
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor")
        self.root.geometry("800x800")

        # Create two tabs: encrypt / decrypt
        self.tab_control = ttk.Notebook(root)
        self.encrypt_tab = ttk.Frame(self.tab_control)
        self.decrypt_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.encrypt_tab, text="Encrypt")
        self.tab_control.add(self.decrypt_tab, text="Decrypt")
        self.tab_control.pack(expand=1, fill="both")

        # Initialize variables
        self.loaded_file = None
        self.processed_content = ""

        '''
        WIDGETS
        '''
        # Encrypt Tab
        self.password_label = ttk.Label(self.encrypt_tab, text="Enter Password:")
        self.password_label.pack()
        self.password_entry = ttk.Entry(self.encrypt_tab, show="")
        self.password_entry.pack()
        self.generate_key_button = ttk.Button(self.encrypt_tab, text="Generate Key", command=self.generate_key)
        self.generate_key_button.pack()
        self.key_label_encrypt = ttk.Label(self.encrypt_tab, text="Generated Key:")
        self.key_label_encrypt.pack()
        self.key_display = tk.Label(self.encrypt_tab, text="")
        self.key_display.pack()
        self.copy_key_button = ttk.Button(self.encrypt_tab, text="Copy Key", command=self.copy_key)
        self.copy_key_button.pack()

        # Decrypt Tab
        # Don't need to generate a key
        self.key_label_decrypt = ttk.Label(self.decrypt_tab, text="Enter Decryption Key:")
        self.key_label_decrypt.pack()
        self.key_entry_decrypt = ttk.Entry(self.decrypt_tab, show="")
        self.key_entry_decrypt.pack()

        '''
        FIRST TEXTBOXES - LOADED CONTENTS
        '''
        # ENCRYPT
        self.openbox_plain = tk.Text(self.encrypt_tab, height=15, width=90)
        self.openbox_plain.pack()

        # DECRYPT
        self.openbox_cipher = tk.Text(self.decrypt_tab, height=15, width=90)
        self.openbox_cipher.pack()

        '''
        FILE PROCESSING BUTTONS
        '''
        # ENCRYPT

        # Frame
        self.button_frame_encrypt = ttk.Frame(self.encrypt_tab)
        self.button_frame_encrypt.pack()

        # Buttons
        self.open_button = ttk.Button(self.button_frame_encrypt, text="Open File", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)
        self.process_button = ttk.Button(self.button_frame_encrypt, text="Encrypt", command=self.process_file)
        self.process_button.pack(side=tk.LEFT)

        # DECRYPT

        # Frame
        self.button_frame_decrypt = ttk.Frame(self.decrypt_tab)
        self.button_frame_decrypt.pack()

        # Buttons
        self.open_button = ttk.Button(self.button_frame_decrypt, text="Open File", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)
        self.process_button = ttk.Button(self.button_frame_decrypt, text="Decrypt", command=self.process_file)
        self.process_button.pack(side=tk.LEFT)

        '''
        SECOND TEXTBOX - PROCESSED CONTENTS
        '''
        # ENCRYPT
        self.savebox_cipher = tk.Text(self.encrypt_tab, height=15, width=90)
        self.savebox_cipher.pack()

        # DECRYPT
        self.savebox_plain = tk.Text(self.decrypt_tab, height=15, width=90)
        self.savebox_plain.pack()

    def generate_key(self):
        self.password = self.password_entry.get()
        if len(self.password) < 1:
            return
        self.key = sha3.generate_key(self.password)
        self.key_display.config(text=self.key)
    
    def copy_key(self):
        root.clipboard_clear()
        root.clipboard_append(self.key)

    def encrypting(self):
        current_tab = self.tab_control.tab(self.tab_control.select(), "text")
        return current_tab == "Encrypt"

    def open_file(self):
        # Open a file and display its content
        self.loaded_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.open_file_path = self.loaded_file

        if self.loaded_file:
           
            # RB to enable display of encrypted ciphertext 
            with open(self.loaded_file, "rb") as file:
                content = file.read()

                if self.encrypting():
                    self.openbox_plain.delete(1.0, tk.END)
                    self.openbox_plain.insert(tk.END, content)

                else:
                    self.openbox_cipher.delete(1.0, tk.END)
                    self.openbox_cipher.insert(tk.END, content)

    def process_file(self):
        # If no key has been inputted, do nothing
        if len(self.key) < 1:
            return
        # If no file has been opened, do nothing
        if self.open_file_path == "":
            return
        elif self.encrypting():
            self.save_file_path = aes.encrypt(self.open_file_path, self.key)
            text = "File processing. Please wait, this may take up to a minute..."
            self.savebox_cipher.delete(1.0, tk.END)
            self.savebox_cipher.insert(tk.END, text)
        else:
            self.save_file_path = aes.decrypt(self.open_file_path, self.key)
            text = "File processing. Please wait, this may take up to a minute..."
            self.savebox_plain.delete(1.0, tk.END)
            self.savebox_plain.insert(tk.END, text)
        
        if self.save_file_path == "":
            return
        elif self.encrypting():
            self.savebox_cipher.delete("1.0", tk.END)
            with open(self.save_file_path, mode = "rb") as file:
                text = file.read()
                self.savebox_cipher.insert(tk.END, text)
        else:
            self.savebox_plain.delete("1.0", tk.END)
            with open(self.save_file_path, mode = "rb") as file:
                text = file.read()
                self.savebox_plain.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()