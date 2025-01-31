from motus import Attempt, Answer, Color
import motus as mt
import sys
##################### traite le hidden choisi ############
dico = mt.Dictionary("data/ods6.txt")

if len(sys.argv) > 1:
    word = sys.argv[1] 
    if not word in dico :
        raise ValueError(f"le mot {word} n'est pas dans le dictionnaire")

if len(sys.argv) < 2:
    lenght = int(input("Entrez la longueur du mot à trouver : "))
    word = dico.sample_of_length(lenght)
    

mot_cachee = mt.Hidden(word)
print(mot_cachee)



