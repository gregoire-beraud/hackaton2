---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  title: 'TP: le jeu de motus'
---

+++ {"tags": ["raises-exception"]}

# le jeu de motus

+++

inspiré d'un jeu télévisé; pour ceux qui ne connaissent pas les règles, on parle d'un jeu qui s'insipre un peu du mastermind, mais avec des mots; il s'agit de trouver un mot caché, on essaie un mot et en réponse on nous dit si chaque lettre est présente et/ou bien placée.

+++

pour plus de détails sur ce jeu, voyez <https://fr.wikipedia.org/wiki/Motus_(jeu_t%C3%A9l%C3%A9vis%C3%A9)>

+++

## les règles

voici un exemple de session, le mot à deviner était `CITRON`

```{image} media/motus-example.png
:align: center
```

ici on a 
* d'abord essayé `CASTOR`; la 'correction' nous a appris que
  * le mot commence par un `C`,
  * qu'il contient un `O` en 5-ème position,
  * qu'il contient un `T` mais pas en 4-éme position,
  * et un `R` mais pas en dernière position,
  * et pas de `A` ni de `S`
* on a ensuite essayé `CINEMA` ou a appris que
  * la seconde lettre est `I`,
  * le mot contient un `N` mais pas en 3-ème position,
  * etc...

les codes de couleur sont donc
* rouge: lettre bien placée
* jaune: lettre mal placée
* bleu (ou blanc, selon les supports): lettre absente

````{admonition} en fait..
:class: admonition-small

**note:** en fait au tout début on vous montre la première lettre, en rouge; mais bon ça ne change pas grand-chose à notre TP
````

+++

### petite subtilité

il faut préciser un peu ce qu'il se passe lorsque l'un des deux mots (le caché, ou la tentative) contient des lettres en double

la règle est que on commence par donner autant de rouges que possible, puis ces lettres-là sont enlevées du décompte; 
puis on donne ensuite autant de jaunes que possible, et à chaque fois les lettres sont enlevées du décompte;

+++

c'est  ainsi que par exemple, avec le mot caché `addition` on obtient la correction suivante (la dernière ligne est uniquement explicative)  
```{image} media/example-addition.svg
:align: center
```

vous remarquez que la réponse contient un `d` bleu, alors qu'il y a deux `d` dans le mot à deviner, mais comme ils ont déjà été 'consommés' pour les deux `d` rouges, le troisième `d` est considéré comme absent.

+++

autre exemple, le mot caché est `escarcelle`  
```{image} media/example-escarcelle.svg
:align: center
```

vous remarquez que la réponse contient

* un `e` rouge en 1ème position, 
* un `e` jaune en 6-ième position qui correspond à la 7-ème position du mot caché, 
* et aussi un `e` bleu en 9-ème position, **malgré le fait que le mot caché contient .. plein de `e`** !

ce qui signifie entre autres qu'il ne suffit pas trouver une lettre en bleu dans la réponse pour en déduire qu'elle n'est pas présente dans le mot, comme ce contrexemple nous le montre bien

+++

## ce qui est fourni

{download}`commencez par télécharger le zip<./ARTEFACTS-motus.zip>`
dans lequel vous trouverez

* un dictionnaire (dans `data/ods6.txt`)
* un module `motus.py` qui contient des morceaux de logique

```{code-cell} ipython3
# FYI this data comes from this URL
from pathlib import Path 

print(Path("data/ods6.url").open().read())
```

## étape 1: l'ordi anime le jeu

dans un premier temps:
* lisez le module `motus.py`
* utilisez le pour écrire un fichier `main.py` qui implémente un jeu dans lequel l'ordi se contente de vous faire jouer:
  * il demande un nombre de lettres
  * il tire au sort un mot
  * il montre la première lettre, et les autres sont en gris
  * l'humain propose un mot, l'ordi donne la "correction", etc.. jusqu'à ce que mot soit trouvé
 
on lance le jeu avec
```bash
python main.py
```

+++

## étape 2: on lui passe un paramètre

ça peut être utile, au moins pour le debug, de pouvoir choisir le mot caché, c'est-à-dire de pouvoir lancer
```bash
python motus.py citron
```

ça vous fera gagner du temps pour la suite

+++

## étape 3: debugging

en fait si vous rejouez les exemples ci-dessus, surtout avec les lettres multiples, vous allez voir que le code de `motus.py` est un peu buggé, votre mission est de le corriger

+++

## étape 4: de l'aide

en option, l'humain peut demander à l'ordi un indice; à vous de voir, on peut imaginer par exemple

* si on tape `?help`, le jeu affiche un readme qui résume .. les commandes de triche
* si on tape `?howmany`, le jeu affiche combien de mots conviennent dans le dictionnaires
* si on tape `?words`, le jeu affiche les mots qui conviennent
* si on tape `?letters`, le jeu affiche, si on en trouve, les lettres que l'on peut déduire à ce stade de la recherche
* ...

+++

## discussion: refactoring ?

on voudrait maintenant que l'ordi puisse indifféremment: 

* ou bien animer le jeu (comme on vient de le faire)
* ou bien jouer avec un humain qui anime le jeu,
* ou remplir les deux rôles et jouer contre lui-même...

est-ce que le code est bien adapté pour ça ?  
sinon comment le restructurer pour ce type d'usages ?

+++

## une librairie utile: `colorama`

+++

pour l'affichage j'ai utilisé ci-dessus la librairie `colorama`, voici quelques exemples, cherchez la documentation si vous avez besoin de plus de détails

```{code-cell} ipython3
# as you can see in the doc, windows users will probably need to do this
from colorama import just_fix_windows_console
just_fix_windows_console()
```

```{code-cell} ipython3
from colorama import Back, Style
```

```{code-cell} ipython3
# on peut l'utiliser comme ceci
print(f"{Back.RED} C  I {Back.YELLOW} N {Back.BLUE} E M A {Style.RESET_ALL}")
```

```{code-cell} ipython3
# ou encore
from colorama import Back, Style
print(f"{Back.RED} C {Style.RESET_ALL} {Back.RED} I {Style.RESET_ALL} "
      f"{Back.YELLOW} N {Style.RESET_ALL} {Back.BLUE} E {Style.RESET_ALL} "
      f"{Back.YELLOW} M {Style.RESET_ALL} {Back.YELLOW} A {Style.RESET_ALL}")
```

***
