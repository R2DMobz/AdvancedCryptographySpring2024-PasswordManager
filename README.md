# AES256-SHA3 Enabled File Encryption

An application that enables users to open, encrypt, decrypt, and save files. 

Encryption and decryption is handled using AES256.

Key generation for AES is handled using SHA3.

The application is implemented in Python using Tkinter for the GUI.

## User's guide

To run the application, execute the command:

```
python gui.py
```

The encrypted and decrypted files will save to the same directory the application is running in.

When encrypting, enter a password, generate a key, and copy the key to your clipboard. 

When decrypting, paste the key you generated when encrypting. You may have to use ctrl+v. 

If you run the application multiple times using the same original text file, you must delete the encrypted and decrypted text files first. Otherwise, the program won't be able to create new ciphertext and plaintext files.