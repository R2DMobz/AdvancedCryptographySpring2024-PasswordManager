# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 13:07:38 2024

@author: Servies_PC
"""
import sha3 as h
import secrets

import psycopg2
from psycopg2 import Error

# Function to generate a random 256-bit key
def generate_key(size=16):
    # Generate 32 bytes (256 bits) of random data
    random_bytes = secrets.token_bytes(size)
    # Convert the random bytes to a hexadecimal string
    password = random_bytes.hex()
    return password

def generate_salt(size=16):
    random_bytes = secrets.token_bytes(size)
    return random_bytes.hex()

# Function to hash the key using SHA-3 (256-bit)
def hash_key(key, salt):
    hash_key = h.sha_3(key, 512, salt)
    store_in_database(hash_key, salt)
    return hash_key

# Function to store the hashed key and salt in PostgreSQL database
def store_in_database(hashed_key, salt):
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            user ="postgres",
            password = ,
            host = "localhost",
            port = "5432",
            database = "CS7530passwords"
        )

        cursor = connection.cursor()
        hex_hash_key = hashed_key.hex()
        # Execute the SQL command to insert hashed key and salt
        cursor.execute("INSERT INTO cs7530passwords.keys (hashed_keys, salt) VALUES (%s, %s);", (hex_hash_key, salt))
        
        # Commit changes
        connection.commit()
        print("Data stored successfully in PostgreSQL")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # Close database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
# # Generate key and salt
# key = generate_key(32)
# salt = generate_salt(32)

# # Hash the key
# hashed_key = hash_key(key, salt)
