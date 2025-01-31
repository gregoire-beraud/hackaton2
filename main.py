from motus import Attempt, Answer, Color
import motus as mt
import sys
 
#On demande à l'utilisateur de rentrer la longueur du mot à trouver
#On génère un mot de la longueur demandée présent dans le dictionnaire


##################### traite le hidden choisi ############
dico = mt.Dictionary("data/ods6.txt")

if len(sys.argv) > 1:
    word = sys.argv[1] 
    if not word in dico:
        raise ValueError(f"Le mot {word} n'est pas dans le dictionnaire")
else:
    length = int(input("Entrez la longueur du mot à trouver : "))
    word = dico.sample_of_length(length)
    

mot_cachee = mt.Hidden(word)
print(mot_cachee)
###########################################################

hidden = mt.Hidden(word)
print(word[0])
for i in range(10):
    typed = input("Entrez un mot : ")
    attempt = hidden.attempt(typed) #On a un objet de type Attempt  
    print(attempt)

