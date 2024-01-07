from key_generator import *
from hash import *
from encryption import *
from decryption import *
from datetime import datetime, timedelta
import os
import re
from colorama import Fore, Style

def print_serpent():
    serpent = """
           /^\/^\\
         _|__|  O|
\/     /~     \_/ \\
 \____|__________/  \\
        \_______      \\
                `\     \                 \\
                  |     |                  \\
                 /      /                    \\
                /     /                       \\
              /      /                         \ \\
             /     /                            \  \\
           /     /             _----_            \   \\
          /     /           _-~      ~-_         |   |
         (      (        _-~    _--_    ~-_     _/   |
          \      ~-____-~    _-~    ~-_    ~-_-~    /
            ~-_           _-~          ~-_       _-~
               ~--______-~                ~-___-~   
"""
    print(serpent)

def menu(user):
    other_user = "alice" if user == "bob" else "bob"
    print("Mini PaI options")
    print("->1<- Encrypt / decrypt message.")
    print("->2<- Generate public / private key.")
    print("->3<- Generate and sign a certificate.")
    print(f"->4<- Verifying {other_user} certificate.")
    print(f"->5<- Send an asynchronous message to {other_user}.")
    print(f"->6<- Ask for a knowledge proof.")
    print("->7<- Decrypt all messages from message file.")
    print("->8<- Clear message box.")
    print("->9<- Change user.")
    print("->10<- Reload the menu.")
    print("->0<- Quit.")

# Function for menu choice
def choix(): 
    choix = input("\nChoose a valid number : ")
    return choix

# Function for creating the tree and verifying its integrity every time an action occurs
def verify_tree():
    directories = ['alice', 'bob', 'tier']
    directories_no = [directory for directory in directories if not os.path.exists(directory)]
    if directories_no:
        reponse = input(f"The infrastructure doesn't exist, do you want to create it ? (y/N) ").lower()
        if reponse =='y':
            for directory in directories_no:
                os.makedirs(directory)
            message = os.path.join("alice", "messages")   
            with open(message, 'w'):
                pass
            message = os.path.join("bob", "messages")   
            with open(message, 'w'):
                pass
            n, e, d = generate_asymetrical(512)
            message = os.path.join("tier", "id_serp")  
            with open(message, 'w') as f:
                f.write('\n'.join([str(n), str(d)]))
            message = os.path.join("tier", "id_serp.pub")  
            with open(message, 'w') as f:
                f.write('\n'.join([str(n), str(e)]))
            certificates = os.path.join("tier", "certificates")  
            os.makedirs(certificates)
        else:
            exit()
        print("Infrastructure created.")
    return True

# Function to choose the user at the beginning
def verify_user():
    while True:
        reponse = input("Which user are you ? Alice or Bob ? \n>> ").lower()
        if reponse in ['alice', 'bob']:
            return reponse
        else:
            print("Error : Invalid choice. Choose between Alice and Bob")

# Function to verify if asymetrial keys exists
def verify_keys_exist(user):
    key_filename = f"id_serp"
    public_key_filename = f"{key_filename}.pub"

    if os.path.exists(os.path.join(user, key_filename)) and os.path.exists(os.path.join(user, public_key_filename)):
        return True
    else:
        return False

# Function to take last asymetrical key generated for a given user on the trust tier keys file
def search_user_in_pubkeyfile(user_search):
    filepath="tier/pub_keys_file"
    with open(filepath, 'r') as file:
        lignes = file.readlines()
        for ligne in reversed(lignes):
            champs = ligne.strip().split(';')
            if champs[0].lower() == user_search.lower():
                return ligne
        return False

# Regex for valid email
def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_pattern, email) is not None

# Regex for valid birth date
def is_valid_birthdate(birthdate):
    birthdate_pattern = r'^\d{1,2}/\d{1,2}/\d{4}$'
    return re.match(birthdate_pattern, birthdate) is not None

# Function to verify if certificate exists on tier and user side for a given user
def check_generated_certificate(username):
    if os.path.exists(os.path.join(username, "serp.cert")) and os.path.exists(os.path.join("tier", "certificates", username + ".cert")):
        return True
    else:
        return False
    
# Function to generate a cerificate given some personal information about the users
    
def generate_sign_certificate(mail, born, n , e, utilisateur):
    print("Generating certificate...")
    concat = utilisateur + mail + born + n + e
    sha1hash=sha1(concat)
    hash_int = int(sha1hash, 16)
    # Encrypt concatenation with tier private key
    filepath="tier/id_serp"
    with open(filepath, 'r') as f:
        lignes = f.readlines()
        if len(lignes) >= 2:
            n_tier = lignes[0].strip()
            d_tier = lignes[1].strip()
        else: 
            print("Tier keys are not valid.")
    signature = encrypt_rsa(hash_int, int(n_tier), int(d_tier))
    # Add an expiration date for certificate
    expiration = datetime.now() + timedelta(days=1)
    path = os.path.join(utilisateur, "serp.cert")
    # Write everything in both files (user and tier)
    with open(path, 'w') as f:
        f.write("USER: " + utilisateur + "\n")
        f.write("MAIL ADDRESS: " + mail + "\n")
        f.write("USER BITHDAY: " + born + "\n")
        f.write("PUBLIC KEY: " + n + "," + e + "\n")
        f.write("SIGNATURE: " + str(signature) + "\n")
        f.write("EXPIRATION DATE: " + str(expiration))
    user_cert= utilisateur + ".cert"
    path = os.path.join("tier", "certificates", user_cert )
    with open(path, 'w') as f:
        f.write("USER: " + utilisateur + "\n")
        f.write("MAIL ADDRESS: " + mail + "\n")
        f.write("USER BITHDAY: " + born + "\n")
        f.write("PUBLIC KEY: " + n + "," + e + "\n")
        f.write("SIGNATURE: " + str(signature) + "\n")
        f.write("EXPIRATION DATE: " + str(expiration))

# Function to verify if our own certificate is valid by comparing it with tier one
def valid_own_certificate(utilisateur):
    if check_generated_certificate(utilisateur):
        path1 = os.path.join(utilisateur, "serp.cert")
        user_cert= utilisateur + ".cert"
        path2 = os.path.join("tier", "certificates", user_cert )
        with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
            content1 = f1.read()
            content2 = f2.read()
            # Verifying additional informations such as expiration date and public key compare
        with open(path1, 'r') as f: 
            lines = f.readlines()
            key_cert_n = int(lines[3].split(":")[1].replace(" ", "").split(",")[0])
            key_cert_e = int(lines[3].split(":")[1].replace(" ", "").split(",")[1])
            expiration_line = lines[5].split(":")[1:]
            expiration_str = ":".join(expiration_line).strip()
            expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d %H:%M:%S.%f")
            date_now = datetime.now()
        pub_key_path=os.path.join(utilisateur, "id_serp.pub")
        with open(pub_key_path, 'r') as f:
            lines = f.readlines()
            key_pub_file_n = int(lines[0].strip())
            key_pub_file_e = int(lines[1].strip())

        if content1 == content2:
            if date_now < expiration_date:
                if key_pub_file_n == key_cert_n: 
                    if key_pub_file_e == key_cert_e:
                        return True
                    else: 
                        return False
                else: 
                    return False
            else: 
                return False
        else:
            return False
    else: 
        return False

# Function to validate any user certificate by comparing the hashes (tier on is by decrypting with his public key, owner by taking its informations and hashing it)
def valid_user_certificate(utilisateur):
    if check_generated_certificate(utilisateur):
        # Path 1 is user certificate on user dir
        path1 = os.path.join(utilisateur, "serp.cert")
        user_cert= utilisateur + ".cert"
        # Path 2 is user certificate on tier dir
        path2 = os.path.join("tier", "certificates", user_cert )
        # Path 3 is tier public key (used to decrypt)
        path3 = os.path.join("tier", "id_serp.pub")
        with open(path3, 'r') as f:
            lignes = f.readlines()
            if len(lignes) >= 2:
                n_tier = lignes[0].strip()
                e_tier = lignes[1].strip()
            else: 
                print("Tier keys are not valid.")
        # Taking user informations, concatenate and hashs it
        with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
            content1 = f1.readlines()
            user = content1[0].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", "")
            mail = content1[1].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", "")
            born = content1[2].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", "")
            n = str(content1[3].decode('utf-8').split(":")[1].replace(" ", "").split(",")[0])
            e = str(content1[3].decode('utf-8').split(":")[1].replace(" ", "").split(",")[1])
            #Compute hash, convert into string
            concat = (user + mail + born + n + e).replace("\n", "")
            sha1_user=sha1(concat)
            sha1_user_int=int(sha1_user, 16)
            # Get expiration date
            content2 = f2.readlines()    
            expiration_line = content2[5].decode('utf-8').split(":")[1:]
            expiration_str = ":".join(expiration_line).strip()
            expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d %H:%M:%S.%f")
            date_now = datetime.now()
            # Decrypt signature and compare it with previous computed hash
            signature = int(content2[4].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", ""))
            sh1sign_int=decrypt_rsa(signature, int(n_tier), int(e_tier) )
        if sh1sign_int == sha1_user_int:
            if date_now < expiration_date:
                if valid_own_certificate(utilisateur):
                    return True, "ok"
                else: 
                    return False, "sync"
            else: 
                return False, "exp"
        else: 
            return False, "sign"
    else: 
        return False, "file"

# Main function for user choices and basic algorithms
def main():
    # Verifying basic informations at each loops
    verify_tree()
    user = verify_user()
    print_serpent()
    menu(user)
    check_generated_certificate(user)
    while True:  
        # Printing verified infos
        print(f"\nUser: {Fore.BLUE}{user}{Style.RESET_ALL}")
        if verify_tree():
            print(f"Architecture:[{Fore.GREEN}V{Style.RESET_ALL}]")
        else: 
            verify_tree()
        if verify_keys_exist(user):
            print(f"Asymetrical keys: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else:
            print(f"Asymetrical keys: [{Fore.RED}X{Style.RESET_ALL}]")
        if check_generated_certificate(user):
            print(f"Certificate generated: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else: 
            print(f"Certificate generated: [{Fore.RED}X{Style.RESET_ALL}]")
        if valid_own_certificate(user):
            print(f"Valid user certificate: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else: 
            print(f"Valid user certificate: [{Fore.RED}X{Style.RESET_ALL}]")
        user_choice = choix()
        match user_choice:
            case '1':
                print("Do you want to encrypt or decrypt a message ?")
                print("->1<- Encrypt a message.")
                print("->2<- Decrypt a message.")
                print("->3<- Generate a symetrical key.")
                choice = choix()
                match choice:
                    case '1':
                        message = input("Enter the message you want to encrypt :")
                        key = input('Enter the symetrical key :')
                        if len(key) != 256 or not all(bit in '01' for bit in key):
                            print("The key should be a binary string of length 256.")
                        else:
                            encrypted_message = encrypt(message, key)
                            print("Message chiffré: ", encrypted_message)

                    case '2':
                        cypher = input("Enter the encrypted message you want to decrypt :")
                        key = input('Enter the symetrical key :')
                        if len(cypher) != 256 or not all(bit in '01' for bit in cypher):
                            print("The encrypted message should be a binary string of length 256.")
                        elif len(key) != 256 or not all(bit in '01' for bit in key):
                            print("The key should be a binary string of length 256.")
                        else:
                            decrypted_message = decrypt(cypher, key)
                            print("Message dechiffré: ", decrypted_message)
                    case '3':
                        sym_key = generate_serpent_key()
                        print("Symetrical key: ", sym_key)
                    case _:
                        print("Non valid choice. Enter a valid number.")

            case '2':
                # generating asymetrical keys and sending it to user repo and tier repo
                print(f"{Fore.RED}Creating public and private keys...{Style.RESET_ALL}")
                n, e, d = generate_asymetrical(512)
                user_directory = user
    
                # Creating the file for private
                private_key_file = os.path.join(user_directory, 'id_serp')
                with open(private_key_file, 'w') as f:
                    f.write('\n'.join([str(n), str(d)]))
                # Creating the file for public
                public_key_file = os.path.join(user_directory, 'id_serp.pub')
                with open(public_key_file, 'w') as f:
                    f.write('\n'.join([str(n), str(e)]))
                print(f"{Fore.RED}Generated and saved keys for {user}{Style.RESET_ALL}.")
                # Sending the key to tier file
                print(f"{Fore.RED}Sending keys to trust tier{Style.RESET_ALL}.")
                with open("tier/pub_keys_file", 'a') as f:
                    f.write(';'.join([user,str(n), str(e)])+"\n")
            case '3':
                # Verifying infos and asking for mail and birth date before creating the certificate
                if verify_keys_exist(user):
                    if os.path.exists("tier/id_serp"): 
                        while True: 
                            mail= input("Enter your email adress, 0 to quit\n")
                            if is_valid_email(mail):
                                born= input("Enter your birth date (format : DD/MM/YYYY), 0 to quit\n")
                                if is_valid_birthdate(born):
                                    lignes= search_user_in_pubkeyfile(user)
                                    n=(lignes.strip().split(';')[1])
                                    e=(lignes.strip().split(';')[2])
                                    generate_sign_certificate(mail, born, n, e, user)
                                    break
                                elif born =="0":
                                    break
                                else: 
                                    print(f"{Fore.RED}Invalid birth date. Enter your birth date with DD/MM/YYYY format.{Style.RESET_ALL}")
                            elif mail =="0":
                                break
                            else:
                                print(f"{Fore.RED}Invalid email. Enter a valid email address.{Style.RESET_ALL}")
                    else: 
                        print("Trust tier does not have private key to sign")
                else: 
                    print("You need public/private keys to generate the certificate.")
            case '4':
                # User the we are verifying is always the other as our own user
                other_user = "alice" if user == "bob" else "bob"
                print(f"Certificate verification for {other_user}.")
                # Just using the function to verify and printing it
                result, reason = valid_user_certificate(other_user)
                if result: 
                    print(f"{Fore.GREEN}Certificate of {other_user} valid{Style.RESET_ALL}.")
                else: 
                    if reason == "sign":
                        print(f"{Fore.RED}Certificate of {other_user} invalid, invalid signature{Style.RESET_ALL}.")
                    elif reason == "file":
                        print(f"{Fore.RED}Certificate of {other_user} invalid, certificate doesn't exist{Style.RESET_ALL}.")
                    elif reason == "exp":
                        print(f"{Fore.RED}Certificate of {other_user} invalid, expired certificate{Style.RESET_ALL}.")
                    elif reason == "sync":
                        print(f"{Fore.RED}Certificate of {other_user} invalid, lost synchronysation between user and tier{Style.RESET_ALL}.")
            case '5':
                # Switching there also to send to other user
                other_user = "alice" if user == "bob" else "bob"
                # Using the function to verify both sending and receiving keys
                if search_user_in_pubkeyfile(other_user):
                    # Generating secret key
                    print("Generating secret key...")
                    sym_key = generate_serpent_key()
                    message = os.path.join(user, "sym_key") 
                    with open(message, 'w') as f:
                        f.write(sym_key)
                    print("Encrypting secret key with public key.")
                    sym_key_int = int("".join(map(str, sym_key)), 2)
                    lignes= search_user_in_pubkeyfile(other_user)
                    n=int(lignes.strip().split(';')[1])
                    e=int(lignes.strip().split(';')[2])
                    cle_symetrique_chiffree = encrypt_rsa(sym_key_int, n, e)
                    plain_text=input("Which message to you want to send ?\n")
                    print(f"{Fore.RED}Encrypting message with symetrical key{Style.RESET_ALL}.") 
                    encrypted_message = encrypt(plain_text, sym_key)
                    if user == "bob":
                        crypt_key = os.path.join("alice", "messages") 
                    elif user == "alice":
                        crypt_key = os.path.join("bob", "messages") 
                    print(f"{Fore.RED}Sending secret key and encrypted message{Style.RESET_ALL}...")
                    date_now = datetime.now()
                    with open(crypt_key, 'a') as f:
                        sym_key = str(cle_symetrique_chiffree) + "," + encrypted_message + "," + str(date_now) + "," + user + "\n"
                        f.write(sym_key)
                else:
                    print(f"One or both users don't have asymetrical keys.")                  
            case '6':
                print("Asking for proof of knowledge...")
                # Getting public tier key
                filepath="tier/id_serp.pub"
                with open(filepath, 'r') as f:
                    lignes = f.readlines()
                    if len(lignes) >= 2:
                        n_tier = lignes[0].strip()
                        e_tier = lignes[1].strip()
                # Choosing the message we want to send to verify (random) and encrypt it with public key
                proof_init = random.randint( 0, 10**20 )
                private=encrypt_rsa(proof_init, int(n_tier), int(e_tier))
                # In real life we would send it to tier and he would to the following lines
                filepath="tier/id_serp"
                with open(filepath, 'r') as f:
                    lignes = f.readlines()
                    if len(lignes) >= 2:
                        n_tier = lignes[0].strip()
                        d_tier = lignes[1].strip()
                decrypted_proof=decrypt_rsa(private, int(n_tier), int(d_tier))
                # We now compare both results and see if they are the same
                if proof_init == decrypted_proof: 
                    print(f"{Fore.GREEN}Verified proof{Style.RESET_ALL}.")
                else: 
                    print(f"{Fore.RED}Invalid proof{Style.RESET_ALL}.")
            case '7':
                print("\n")
                # Reading private key
                path=os.path.join(user, "id_serp" )
                with open(path, 'r') as f:
                    lignes = f.readlines()
                    if len(lignes) >= 2:
                        n = lignes[0].strip()
                        d = lignes[1].strip()
                # Reading message file line by line
                pathmess = os.path.join(user, "messages" )
                with open(pathmess, 'r') as f: 
                    linesmess = f.readlines()
                if len(linesmess) > 0: 
                    for ligne in linesmess:
                        champs = ligne.strip().split(',')
                        encrypted_sym_key = champs[0] 
                        encrypted_message = champs[1]
                        date=champs[2]
                        other_user=champs[3]
                        int_sym_key=decrypt_rsa(int(encrypted_sym_key), int(n), int(d) )
                        bin_sym_key=bin(int_sym_key)
                        sym_key=bin_sym_key.replace("0b", "")
                        decrypted_message = decrypt(encrypted_message, sym_key)
                        print(f"{Fore.BLUE}Message received from {other_user} at date {date} {Style.RESET_ALL}:")
                        print(decrypted_message + "\n")
                else: 
                    print("You dont have any message :(")
            case '8':
                delete = input("Do you really want to delete all messages, you wont be able to retreive them after : y/N\n").lower()
                if delete == "y":
                    print("clearing message file...")
                    pathmess = os.path.join(user, "messages" )
                    with open(pathmess, 'w') as f:
                        f.write("")
            case '9': 
                user = verify_user()
                print(f"User: {Fore.BLUE}{user}{Style.RESET_ALL}")
            case '10': 
                menu(user)
            case '0' | 'quit' | 'quitter' | 'q' | 'exit':
                print("Au revoir !")
                exit()  # Quit the program if user enter specific fields
            case _:
                print("Non valid choice. Enter a valid number.")
        
        input("\n\nPress Enter...\n\n")

if __name__ == "__main__":
    main()