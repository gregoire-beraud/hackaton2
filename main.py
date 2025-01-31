import motus as mt
import sys 

#On demande à l'utilisateur de rentrer la longueur du mot à trouver
#On génère un mot de la longueur demandée présent dans le dictionnaire


##################### traite le hidden choisi ############
dico = mt.Dictionary("data/ods6.txt")

if len(sys.argv) > 1:
    word = sys.argv[1] 
    length = len(word)
    if not dico.__contains__(word):
        raise ValueError(f"Le mot {word} n'est pas dans le dictionnaire")

if len(sys.argv) < 2:
    length = int(input("Entrez la longueur du mot à trouver : "))
    word = dico.sample_of_length(length)
    
#print(mot_cachee)
###########################################################

hidden = mt.Hidden(word)
print(mt.Hidden(word[0]))
attempts = []

for i in range(length):

    typed = input("Entrez un mot : ")
    if typed == "?lettre":
        print(hidden.indice_lettre(attempts))
    else:

        if typed not in dico:
            print("Perdu ! Le mot n'est pas dans le dictionnaire")
            print(f"Le mot à trouver était : {word}")
            break
            

        if len(typed) != len(word):
            print("Perdu ! La longueur du mot n'est pas correcte")
            print(f"Le mot à trouver était : {word}")
            break

        else:
            attempt = hidden.attempt(typed) #On a un objet de type Attempt  
            print(attempt)
            attempts.append(attempt)

            if typed == word:
                print("Bravo ! C'est gagné")
                break
            
            if i == length-1:
                print("Perdu ! Vous avez épuisé vos essais")
                print(f"Le mot à trouver était : {word}")
                
