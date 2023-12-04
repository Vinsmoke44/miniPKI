from async_message import *
from crypt_decrypt import *
from verify_certificate import *
from sign_certificate import *
from proof_knowledge import *
from doc_chest import *
from key_generator import *
import time

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
    print("->8<- ")
    print("->9<- ")
    print("->0<- I WANT IT ALL !! I WANT IT NOW !! SecCom from scratch?.")
    

    choix = input("Entrez le numéro de votre choix : ")
    return choix

def main():

        afficher_serpent()
        choix = menu()

        if choix == "1":
            print("Quel message voulez-vous chiffrer/déchiffrer ?")
        elif choix == "2":
            print("Début du processus de création d'un couple de clés publique / privée...")
        elif choix == "3":
            print("Vous avez besoin d'un certificat...")
        elif choix == "4":
            print("Vérifions ce certificat...")
        elif choix == "5":
            print("Quel document voulez-vous enregistrer dans le coffre-fort ?")
        elif choix == "6":
            print("Quel message souhaitez-vous envoyer ?")
        elif choix == "7":
            print("Preuve de connaissance")
        elif choix == "8":
            print("En construction...")
        elif choix == "9":
            print("En construction...")
        elif choix == "0":
            print("Au revoir !")
        else:
            print("Choix non valide. Veuillez entrer un numéro valide.")

if __name__ == "__main__":
    main()

def pading(message):
    padded_message = message + '1'
    original_length = len(message)
    padding_length = 128 - (original_length + 1) % 128
    padded_message += '0' * padding_length
    if original_length % 128 == 0:
        padded_message += '0' * 128   
    return padded_message

def text_to_bits(text):
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def bits_to_text(bits):
    text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
    return text

def segment(bits):
    #divise en blocs de 128 bits
    blocks = [bits[i:i+128] for i in range(0, len(bits), 128)]

    # Applique le bourrage à la fin de la dernière partie si nécessaire
    last_block_index = len(blocks) - 1
    blocks[last_block_index] = pading(blocks[last_block_index])
    return blocks

def desegment(block):
    bites=""
    for i in block: 
        bites += i
    return bites

# Test pour verifier la validité des messages
# message=input("Rentrez votre message\n")
# bits=text_to_bits(message)
# block=segment(bits)
# for i in block: 
#     print(i)
# time.sleep(2)
# bites = desegment(block)
# dcrypt=bits_to_text(bites)
# print(dcrypt)

# test=input("Entrez binaire\n")
# dcode=bits_to_text(test)
# print(dcode)


