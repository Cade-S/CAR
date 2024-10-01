from cryptography.fernet import Fernet          #For encryption
import random                                   #For random shifting for ciphering
import json                                     #For file manipulation
import colorama                                 #See below
from colorama import Fore, Back, Style, init    #For colored text
init()                                          #Keep for colored text implementation on Windows devices







def main():
    #WARNING! IF YOU ARE READING THIS, YOU MAY BE DUMB!
    print(Fore.WHITE + Back.BLUE + Style.BRIGHT) #+ Style.BRIGHT)
    print('''
===============================================================================================
*                                                                                             *
*                                                                                             *
*    .d8888b.        d8888 8888888b.        .d8888b.  d8b          888                        *
*   d88P  Y88b      d88888 888   Y88b      d88P  Y88b Y8P          888                        *
*   888    888     d88P888 888    888      888    888              888                        *
*   888           d88P 888 888   d88P      888        888 88888b.  88888b.   .d88b.  888d888  *
*   888          d88P  888 8888888P"       888        888 888 "88b 888 "88b d8P  Y8b 888P"    *
*   888    888  d88P   888 888 T88b        888    888 888 888  888 888  888 88888888 888      *
*   Y88b  d88P d8888888888 888  T88b       Y88b  d88P 888 888 d88P 888  888 Y8b.     888      *
*    "Y8888P" d88P     888 888   T88b       "Y8888P"  888 88888P"  888  888  "Y8888  888      *
*                                                         888                                 *
*        a          t          J                          888                                 *
*        d          t                                     888                                 *
*        e          i          N                                                              *
*                   c          o                                                              *
*                   u          r                                                              *
*                   s          r                           Version:  0.1                      *
*                              i                           For CPSC 3555                      *
*                              s                                                              *
*                                                                                             *
===============================================================================================

    ''')
    running = True

    while running == True:
        print(Style.NORMAL +'''


1. Encrypt a message

2. Decrypt a message

3. Exit
'''
        )
        print(Back.MAGENTA + Style.BRIGHT)
        inp = input("::")
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT)
        if inp == "1":
            message = input("Enter a message to encrypt::")
            shift1 = random.randint(1, 27)
            shift2 = random.randint(-999, 999)
            ciphered_message = encrypt(message, shift1, shift2)
            print(Fore.GREEN + f"Your Ciphered message is: {ciphered_message}")
            print(Fore.YELLOW + '''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! You must know the ciphered message AND the key to decrypt it!!
!!                All inputs are case-sensitive                !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
''')
            print(Fore.WHITE)
        
        elif inp == "2":
            all_data = load_data()
            key_str = input("Enter the key to decrypt: ")
            ciphered_message = input("Enter the ciphered message: ")


            entry = None
            for data_entry in all_data:
                if data_entry['key'] == key_str:  # Compare keys
                    entry = data_entry
                    break

            if entry:
                try:
                    decrypted_var1, decrypted_var2 = decrypt_entry(key_str, entry)
                    original_message = decrypt(ciphered_message, int(decrypted_var1), int(decrypted_var2))
                    print(Fore.GREEN +f"Original Message: {original_message}")
                    print(Fore.WHITE)
                except Exception as e:
                    
                    print(Fore.RED + f"Decryption failed: {e}")
                    print(Fore.WHITE)
            else:
                print(Fore.RED + "Key not found in stored entries.")
                print(Fore.WHITE)
        elif inp == "3":
            print(Fore.RED)
            print("Exiting...")
            running = False
                
        else:
            print(Fore.YELLOW + "Sorry, your input was not valid. Please try again.")
            print(Fore.WHITE)



def encrypt(message, shift1, shift2):
    result = ""
    
    for char in message:
        if char.isupper():
            result += chr((ord(char) + shift1 - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift1 - 97) % 26 + 97)
        elif char.isdigit():
            result += shift_digit(char, shift2)
        else:
            result += char

    generate_key(shift1, shift2)
    return result



def shift_digit(char, shift2):
    if char.isdigit():
        shifted_digit = (int(char) + shift2) % 10
        return str(shifted_digit)
    else:
        return char



def generate_key(shift1, shift2):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    var1 = fernet.encrypt(str(shift1).encode())
    var2 = fernet.encrypt(str(shift2).encode())

    entry = {
        'key': key.decode(),
        'var1': var1.decode(),
        'var2': var2.decode()
    }

    try:
        with open('encrypt.json', 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open('encrypt.json', 'w') as file:
        json.dump(data, file, indent=4)

    print(Fore.GREEN + f"Success, your key is: {key.decode()}")
    print(Fore.WHITE)


    
def load_data():
    try:
        with open('encrypt.json', 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                return []
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []



def decrypt_entry(key_str, entry):
    key = key_str.encode()
    fernet = Fernet(key)
    var1 = fernet.decrypt(entry['var1'].encode()).decode()
    var2 = fernet.decrypt(entry['var2'].encode()).decode()
    return var1, var2



def decrypt(ciphered_message, shift1, shift2):
    result = ""
    for char in ciphered_message:
        if char.isupper():
            result += chr((ord(char) - shift1 - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - shift1 - 97) % 26 + 97)
        elif char.isdigit():
            result += shift_digit(char, -shift2)
        else:
            result += char
    return result

if __name__ == "__main__":
    main()












    
