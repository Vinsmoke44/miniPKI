from async_message import *
from crypt_decrypt import *
from verify_certificate import *
from sign_certificate import *
from proof_knowledge import *
from doc_chest import *
from key_generator import *
from send import *
from receive import *
import sys
import os
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
    
Crédit ASCII art : https://www.asciiart.eu/animals/reptiles/snakes
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
        else:
            sys.exit()
        print("Architecture PKI créée")
    return True

def verify_user():
    while True:
        reponse = input("Quel utilisateur êtes-vous ? Alice ou Bob ? ").lower()
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

def main():
    verify_tree()
    utilisateur = verify_user()
    print(f"User: {Fore.BLUE}{utilisateur}{Style.RESET_ALL}")
    afficher_serpent()
    menu()
    while True:  
        print(f"\nUser: {Fore.BLUE}{utilisateur}{Style.RESET_ALL}")
        if verify_tree():
            print(f"Architecture:[{Fore.GREEN}V{Style.RESET_ALL}]")
        if verify_keys_exist(utilisateur):
            print(f"Clés asymetriques: [{Fore.GREEN}V{Style.RESET_ALL}]")
        else:
            print(f"Clés asymetriques: [{Fore.RED}X{Style.RESET_ALL}]")
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
            case '3':
                #case si on en a pas, case si on en a 
                print("Vous avez besoin d'un certificat...")
            case '4':
                # case pour si on a pas de certificat
                print("Vérification du certificat...")
            case '5':
                #case si on a pas de documents
                print("Quel document voulez-vous enregistrer dans le coffre-fort ?")
            case '6':
                print("Quel message souhaitez-vous envoyer ?")
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
            case '0' | 'quit' | 'quitter' | 'q' | 'exit':
                print("Au revoir !")
                sys.exit()  # Quitte le programme si l'utilisateur choisit 0
            case _:
                print("Choix non valide. Veuillez entrer un numéro valide.")
        
        input("\nAppuyez sur Enter pour continuer...\n")

if __name__ == "__main__":
    main()

# message=input("Entrez message\n")
# dcode=message2bits(message)
# print(dcode)
# time.sleep(2)
# mess=bits2message(dcode)
# print(mess)


