import argparse
import getpass
import json
import base64

def simple_cipher(data, key):
    encrypted = ""
    for char in data:
        encrypted += chr(ord(char) + key)
    return encrypted

def simple_decipher(data, key):
    decrypted = ""
    for char in data:
        decrypted += chr(ord(char) - key)
    return decrypted

def load_passwords(key):
    try:
        with open("passwords.json", "r") as f:
            encrypted_data = json.load(f)
        
        decrypted_data = {}
        for account, password in encrypted_data.items():
            decrypted_password = simple_decipher(password, key)
            decrypted_data[account] = decrypted_password
        return decrypted_data
    except FileNotFoundError:
        return {}

def save_passwords(passwords, key):
    encrypted_data = {}
    for account, password in passwords.items():
        encrypted_password = simple_cipher(password, key)
        encrypted_data[account] = encrypted_password

    with open("passwords.json", "w") as f:
        json.dump(encrypted_data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="A simple command-line password manager.")
    parser.add_argument("action", choices=["add", "get", "list"], help="The action to perform.")
    parser.add_argument("--account", help="The account name (for add and get actions).")

    args = parser.parse_args()

    key = 5 

    passwords = load_passwords(key)

    if args.action == "add":
        if not args.account:
            print("Error: The --account argument is required for the 'add' action.")
            return
        
        password = getpass.getpass(f"Enter password for {args.account}: ")
        passwords[args.account] = password
        save_passwords(passwords, key)
        print(f"Password for {args.account} has been added.")

    elif args.action == "get":
        if not args.account:
            print("Error: The --account argument is required for the 'get' action.")
            return
        
        password = passwords.get(args.account)
        if password:
            print(f"Password for {args.account}: {password}")
        else:
            print(f"No password found for {args.account}.")

    elif args.action == "list":
        if not passwords:
            print("No accounts found.")
        else:
            print("Accounts:")
            for account in passwords:
                print(f"- {account}")

if __name__ == "__main__":
    main()
