'''
an api to streamline calling sha3 key generation functions from the front-end
---
created by @nicholaswile (April 16th, 2024 1:56 AM) 
'''

sha3 = __import__("SHA-3")

# Password is created by the user, entered into the GUI, and sent to this function
def generate_key(password):
    data = bytes(password, "utf-8")
    hashed_data = sha3.sha3(data, 256)
    hashed_data_bytes = bytes(bytearray(x % 256 for x in hashed_data))
    # This will be displayed on the GUI and sent to AES
    hash = hashed_data_bytes.hex()
    return hash