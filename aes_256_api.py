'''
an "api" that decouples the encrypt/decrypt steps from the main function in aes_256.py 
so they can easily be called from the gui.py user interface file.
---
created by @nicholaswile
'''

import aes_256

def encrypt(input_path, KEY):
    INPUT_PATH = aes_256.os.path.abspath(input_path)
    for symbol in KEY:
        if ord(symbol) > 0xff:
            print('Invaild key. Try another using only latin alphabet and numbers')
            continue
        
    print('Please wait...')

    time_start = aes_256.time.time()

    # Input data
    with open(INPUT_PATH, 'rb') as f:
        data = f.read()

    # Pad the data
    padded_data = aes_256.pad(data)

    crypted_data = []
    temp = []
    for byte in padded_data:
        temp.append(byte)
        if len(temp) ==     16:
            crypted_data.extend(aes_256.encrypt(temp, KEY))

            del temp[:]
    
    out_path = aes_256.os.path.join(aes_256.os.path.dirname(INPUT_PATH), 'crypted_' + aes_256.os.path.basename(INPUT_PATH))

    msg = 'New encrypted file here:', out_path, '--', aes_256.time.time() - time_start, ' seconds'
    print(msg)

    # Output data
    with open(out_path, 'xb') as ff:
        ff.write(bytes(crypted_data))

    # return msg
    return out_path

def decrypt(out_path, KEY):
    OUT_PATH = aes_256.os.path.abspath(out_path)
        
    time_start = aes_256.time.time()
    
    decrypted_data = []
    temp = []

    # Assume this is a crypted file
    with open(OUT_PATH, 'rb') as f:
        crypted_data = f.read()

    for byte in crypted_data:
        temp.append(byte)
        if len(temp) == 16:
            decrypted_data.extend(aes_256.decrypt(temp, KEY))

            del temp[:]

    # Remove padding
    unpadded_data = aes_256.unpad(bytes(decrypted_data))

    decrypted_out_path = aes_256.os.path.join(aes_256.os.path.dirname(OUT_PATH), 'decrypted_' + aes_256.os.path.basename(OUT_PATH))

    # Output decrypted data
    with open(decrypted_out_path, 'xb') as ff:
        ff.write(unpadded_data)

    msg = 'New decrypted here:', out_path, '--', aes_256.time.time() - time_start, ' seconds. If something is wrong, check the key you entered'
    print(msg)
    #return msg
    return decrypted_out_path