import motus as mt
import sys 
import random as rd

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

hidden = mt.Hidden(word)
print(hidden)
typed = dico.sample_of_length(length)
attempts = []

for i in range(length):
    S = dico.compatible_words(attempts, length)
    if len(S) == 0:
        print("Aucun mot compatible trouvé.")
        break

    typed = list(S)[rd.randint(0, len(S) - 1)]  # On prend un mot compatible au hasard
    attempt = hidden.attempt(typed)
    attempts.append(attempt)

    print(f"Tentative {i+1}: {typed}")
    print(attempt)

    if attempt.success(word):
        print("Félicitations ! Vous avez trouvé le mot.")
        break
else:
    print("Désolé, vous n'avez pas trouvé le mot.")
