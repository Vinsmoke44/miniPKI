from async_message import *
from crypt_decrypt import *
from verify_certificate import *
from sign_certificate import *
from proof_knowledge import *
from doc_chest import *
from key_generator import *
from send import *
from receive import *
from hash import *
from datetime import datetime, timedelta
import os
import re
from colorama import Fore, Style

def afficher_serpent():
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

def menu():
    print("Bonjour ô maître Rémi ! Que souhaitez-vous faire aujourd'hui ?")
    print("->1<- Chiffrer / déchiffrer des messages.")
    print("->2<- Créer un couple de clés publique / privée (générer un grand nombre premier).")
    print("->3<- Signer / générer un certificat.")
    print("->4<- Vérifier un certificat.")
    print("->5<- Enregistrer un document dans le coffre-fort.")
    print("->6<- Envoyer un message (asynchrone).")
    print("->7<- Demander une preuve de connaissance.")
    print("->8<- Creer un block chain")
    print("->9<- I WANT IT ALL !! I WANT IT NOW !! SecCom from scratch?.")
    print("->10<- Re afficher le menu")
    print("->11<- Changer d'utilisateur")
    print("->0<- Quitter")
    
def choix(): 
    choix = input("Entrez le numéro de votre choix : ")
    return choix

def verify_tree():
    directories = ['alice', 'bob', 'tier']
    directories_no = [directory for directory in directories if not os.path.exists(directory)]
    if directories_no:
        reponse = input(f"L'architecture PKI n'existe pas voulez la créer? (O/N) ").lower()
        if reponse =='o':
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
        print("Architecture PKI créée")
    return True

def verify_user():
    while True:
        reponse = input("Quel utilisateur êtes-vous ? Alice ou Bob ? \n>> ").lower()
        if reponse in ['alice', 'bob']:
            return reponse
        else:
            print("Erreur : Choix invalide. Veuillez choisir entre Alice et Bob.")

def verify_keys_exist(user):
    key_filename = f"id_serp"
    public_key_filename = f"{key_filename}.pub"

    if os.path.exists(os.path.join(user, key_filename)) and os.path.exists(os.path.join(user, public_key_filename)):
        return True
    else:
        return False

def search_user_in_pubkeyfile(user_search):
    filepath="tier/pub_keys_file"
    with open(filepath, 'r') as file:
        lignes = file.readlines()
        # Parcourez les lignes à l'envers
        for ligne in reversed(lignes):
            # Divisez la ligne en champs en utilisant le point-virgule comme délimiteur
            champs = ligne.strip().split(';')
            if champs[0].lower() == user_search.lower():
                # Si c'est le cas, imprimez la ligne ou effectuez d'autres actions nécessaires
                return ligne
        return False
    
def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_pattern, email) is not None

# Fonction pour valider la date de naissance
def is_valid_birthdate(birthdate):
    birthdate_pattern = r'^\d{1,2}/\d{1,2}/\d{4}$'
    return re.match(birthdate_pattern, birthdate) is not None

def check_generated_certificate(username):
    if os.path.exists(os.path.join(username, "serp.cert")) and os.path.exists(os.path.join("tier", "certificates", username + ".cert")):
        return True
    else:
        return False
    
def generate_sign_certificate(mail, born, n , e, utilisateur):
    print("Generation du certificat")
    #Generation de la signature
    concat = utilisateur + mail + born + n + e
    sha1hash=sha1(concat)
    print(sha1hash)
    print(concat)
    hash_int = int(sha1hash, 16)
    #Chiffrement du hash avec la clé privé de l'autorité
    filepath="tier/id_serp"
    with open(filepath, 'r') as f:
        lignes = f.readlines()
        if len(lignes) >= 2:
            n_tier = lignes[0].strip()
            d_tier = lignes[1].strip()
        else: 
            print("Clés du tier de confiance non valides")
    signature = encrypt_rsa(hash_int, int(n_tier), int(d_tier))
    print(hash_int, signature)
    expiration = datetime.now() + timedelta(days=1)
    path = os.path.join(utilisateur, "serp.cert")
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

def valid_own_certificate(utilisateur):
    if check_generated_certificate(utilisateur):
        path1 = os.path.join(utilisateur, "serp.cert")
        user_cert= utilisateur + ".cert"
        path2 = os.path.join("tier", "certificates", user_cert )
        with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
            content1 = f1.read()
            content2 = f2.read()
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

def valid_user_certificate(utilisateur):
        path1 = os.path.join(utilisateur, "serp.cert")
        user_cert= utilisateur + ".cert"
        path2 = os.path.join("tier", "certificates", user_cert )
        path3 = os.path.join("tier", "id_serp.pub")
        with open(path3, 'r') as f:
            lignes = f.readlines()
            if len(lignes) >= 2:
                n_tier = lignes[0].strip()
                e_tier = lignes[1].strip()
            else: 
                print("Clés du tier de confiance non valides")
        with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
            content1 = f1.readlines()
            user = content1[0].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", "")
            mail = content1[1].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", "")
            born = content1[2].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", "")
            n = str(content1[3].decode('utf-8').split(":")[1].replace(" ", "").split(",")[0])
            e = str(content1[3].decode('utf-8').split(":")[1].replace(" ", "").split(",")[1])
            #Calcule le hash de la concatenation et le convertit en strings
            concat = (user + mail + born + n + e).replace("\n", "")
            sha1_user=sha1(concat)
            sha1_user_int=int(sha1_user, 16)
            # Recupere la date d'expiration dans le certificat récuperé avec le tier
            expiration_line = content2[5].decode('utf-8').split(":")[1:]
            expiration_str = ":".join(expiration_line).strip()
            expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d %H:%M:%S.%f")
            date_now = datetime.now()
            content2 = f2.readlines()    
            # Dechiffre la signature avec la clé publique du tier et la compare avec le hash calculé avant
            signature = int(content2[4].decode('utf-8').split(":")[1].replace(" ", "").replace("\n", ""))
            sh1sign_int=decrypt_rsa(signature, int(n_tier), int(e_tier) )
            print(sha1_user_int, sh1sign_int)
            if sha1_user_int == sh1sign_int: 
                print("ok")
def main():
    verify_tree()
    utilisateur = verify_user()
    afficher_serpent()
    menu()
    check_generated_certificate(utilisateur)
    while True:  
        print(f"\nUser: {Fore.BLUE}{utilisateur}{Style.RESET_ALL}")
        if verify_tree():
            print(f"Architecture:[{Fore.GREEN}V{Style.RESET_ALL}]")
        else: 
            verify_tree()
        if verify_keys_exist(utilisateur):
            print(f"Clés asymetriques: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else:
            print(f"Clés asymetriques: [{Fore.RED}X{Style.RESET_ALL}]")
        if check_generated_certificate(utilisateur):
            print(f"Certificat généré: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else: 
            print(f"Certificat généré: [{Fore.RED}X{Style.RESET_ALL}]")
        if valid_own_certificate(utilisateur):
            print(f"Certificat utilisateur valide: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else: 
            print(f"Certificat utilisateur valide: [{Fore.RED}X{Style.RESET_ALL}]")
        choice_user = choix()
        match choice_user:
            case '1':
                print("Quel message voulez-vous chiffrer/déchiffrer ?")
                #crypt() -> demande dans cette fonction ce que l'on veux chiffrer dechiffrer et affiche le message
            case '2':
                print("Début du processus de création d'un couple de clés publique / privée...")
                n, e, d = generate_asymetrical(512)
                user_directory = utilisateur
    
                # Créer le fichier pour la clé privée
                private_key_file = os.path.join(user_directory, 'id_serp')
                with open(private_key_file, 'w') as f:
                    f.write('\n'.join([str(n), str(d)]))
                # Créer le fichier pour la clé publique
                public_key_file = os.path.join(user_directory, 'id_serp.pub')
                with open(public_key_file, 'w') as f:
                    f.write('\n'.join([str(n), str(e)]))
                print(f"Clés générées et enregistrées pour {utilisateur}.")
                # Envoyer la clé publique au tier de confiance 
                print("Envoie de la clé publique au tier de confiance")
                with open("tier/pub_keys_file", 'a') as f:
                    f.write(';'.join([utilisateur,str(n), str(e)])+"\n")
            case '3':
                if verify_keys_exist(utilisateur):
                    if os.path.exists("tier/id_serp"): 
                        while True: 
                            mail= input("Veuillez renseigner votre adresse email, 0 pour annuler\n")
                            if is_valid_email(mail):
                                born= input("Veuillez renseigner votre date de naissance sous la forme JJ/MM/AAAA, 0 pour annuler\n")
                                if is_valid_birthdate(born):
                                    lignes= search_user_in_pubkeyfile(utilisateur)
                                    n=(lignes.strip().split(';')[1])
                                    e=(lignes.strip().split(';')[2])
                                    generate_sign_certificate(mail, born, n, e, utilisateur)
                                    break
                                elif born =="0":
                                    break
                                else: 
                                    print(f"{Fore.RED}Date de naissance invalide. Veuillez saisir une date de naissance valide au format JJ/MM/AAAA.{Style.RESET_ALL}")
                            elif mail =="0":
                                break
                            else:
                                print(f"{Fore.RED}Adresse e-mail invalide. Veuillez saisir une adresse e-mail valide.{Style.RESET_ALL}")
                    else: 
                        print("Le tier de confiance n'a pas de clé privé pour signer")
                else: 
                    print("Il vous faut un couple de clé asymetrique afin de génerer/signer un certificat")
            case '4':
                if utilisateur == "bob":
                    user_search="alice"
                elif utilisateur == "alice":
                    user_search="bob" 
                print(f"Verification de certificat de {user_search}")
            case '5':
                #case si on a pas de documents
                print("Quel document voulez-vous enregistrer dans le coffre-fort ?")
            case '6':
                if utilisateur == "bob":
                    user_search="alice"
                elif utilisateur == "alice":
                    user_search="bob" 
                if search_user_in_pubkeyfile(user_search):
                    print("Generation de la clé secrete")
                    sym_key = generate_serpent_key()
                    message = os.path.join(utilisateur, "sym_key") 
                    with open(message, 'w') as f:
                        f.write(sym_key)
                    # print(sym_key)
                    print("Chiffrement de la clé secrete avec la clés public")
                    sym_key_int = int("".join(map(str, sym_key)), 2)
                    lignes= search_user_in_pubkeyfile(user_search)
                    # print(lignes)
                    n=int(lignes.strip().split(';')[1])
                    e=int(lignes.strip().split(';')[2])
                    # print("Clé publique: " + str(n) + ";" + str(e))
                    cle_symetrique_chiffree = encrypt_rsa(sym_key_int, n, e)
                    # print("Clé symétrique chiffrée :", cle_symetrique_chiffree)
                    plain_text=input("Quel message souhaitez-vous envoyer ?\n") 
                    if utilisateur == "bob":
                        crypt_key = os.path.join("alice", "messages") 
                    elif utilisateur == "alice":
                        crypt_key = os.path.join("bob", "messages") 
                    with open(crypt_key, 'a') as f:
                        sym_key = str(cle_symetrique_chiffree) + "," + plain_text +  "\n"
                        f.write(sym_key)
                    print("Envoie de la clé secrete et du message chifré")
                else:
                    print(f"Les 2 utilisateurs n'ont pas crées de clés asymetriques")                  
            case '7':
                print("Demande de preuve de connaissance")
            case '8':
                print("Bloc chain")
            case '9':
                print("Seccom from scratch")
                #creation de clés
                #envoie de la clés secrète
                #création certificat 
                #message asynchrone 
                #verification et signature certificat
            case '10': 
                menu()
            case '11': 
                utilisateur = verify_user()
                print(f"User: {Fore.BLUE}{utilisateur}{Style.RESET_ALL}")
            case '0' | 'quit' | 'quitter' | 'q' | 'exit':
                print("Au revoir !")
                exit()  # Quitte le programme si l'utilisateur choisit 0
            case _:
                print("Choix non valide. Veuillez entrer un numéro valide.")
        
        input("\n\nAppuyez sur Enter pour continuer...\n\n")

if __name__ == "__main__":
    main()